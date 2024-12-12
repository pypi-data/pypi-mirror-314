import ydb


class Query:
    def __init__(self, table, args, kwargs):
        self.args = args
        self.table = table
        self.q = table.select_fields
        self.database = table._database_
        self.view = table.view

    def select(self):
        objects = self[:]
        return [self.table.from_dict(item) for item in objects]

    def count(self):
        self.q = 'count(*) AS c'
        objects = self[:]
        return objects[0]['c']

    def bulk(self, item_list):
        column_types = ydb.BulkUpsertColumns()
        # column_list = []
        for key in item_list[0]:
            if key in self.table.attrs_dict:
                column_types.add_column(key, self.table.attrs_dict[key].ydb_type)
        return self.database.bulk(self.table.table_name, column_types, item_list)

    def delete(self):
        declare = []
        where = []
        params = {}
        i = 0
        for _ in self.args:
            t, field, value = _
            name, param, title = f"{field.name}", f"param{i}", field.title
            if t in ['in']:
                declare.append(f"DECLARE ${param} AS List<{title}>;")
            else:
                declare.append(f"DECLARE ${param} AS {title};")
            params[f'${param}'] = value
            where.append(f'{name} {t} ${param}')
            i += 1
        sql = f'DELETE from {self.table.table_name}'
        if self.view:
            sql += f' view {self.view} '
            self.view = ''
        if declare:
            sql = '\n'.join(declare) + '\n' + sql
        if where:
            sql = sql + '\nWHERE ' + ' AND '.join(where)
        # print(sql)
        return self.database.query(sql, params)

    def get(self):
        objects = self[:2]
        if not objects:
            return None
        if len(objects) > 1:
            raise (Exception, 'Multiple objects were found. Use select(...) to retrieve them')
        return self.table.from_dict(objects[0])

    def _fetch(self, limit=None, offset=None, lazy=False):
        return QueryResult(self, limit, offset, lazy=lazy)

    def _actual_fetch(self, limit, offset):
        declare = []
        where = []
        params = {}
        i = 0
        for _ in self.args:
            t, field, value = _
            # name, title = f"{field.name}", field.title
            name, param, title = f"{field.name}", f"param{i}", field.title
            # print(name, param, title)

            if t in ['in']:
                declare.append(f"DECLARE ${param} AS List<{title}>;")
                if isinstance(value, list) or isinstance(value, set):
                    value = tuple(value)
            elif t == 'is NULL':
                print('is NULL')
            else:
                declare.append(f"DECLARE ${param} AS {title};")
            if t == 'is NULL':
                where.append(f'{name} {t}')
            else:
                params[f'${param}'] = value
                where.append(f'{name} {t} ${param}')
            i += 1
        sql = f'SELECT {self.q} from {self.table.table_name}'
        if self.view:
            sql += f' view {self.view} '
            self.view = ''
        if declare:
            sql = '\n'.join(declare) + '\n' + sql
        if where:
            sql = sql + '\nWHERE ' + ' AND '.join(where)
        # print(sql)
        if self.table.order:
            sql += f' ORDER BY {self.table.order}'
            self.table.order = ''

        sql += f' LIMIT {self.table.limit}'
        self.table.limit = 1000
        self.table.select_fields = '*'
        return self.database.query(sql, params)

    def __iter__(self):
        return iter(self._fetch(lazy=True))

    def __getitem__(self, key):
        if not isinstance(key, slice):
            raise (TypeError, 'If you want apply index to a query, convert it to list first')

        step = key.step
        if step is not None and step != 1:
            raise(TypeError, "Parameter 'step' of slice object is not allowed here")
        start = key.start
        if start is None:
            start = 0
        elif start < 0:
            raise (TypeError, "Parameter 'start' of slice object cannot be negative")
        stop = key.stop
        if stop is None:
            if not start:
                return self._fetch()
            else:
                return self._fetch(limit=None, offset=start)
        if start >= stop:
            return self._fetch(limit=0)
        return self._fetch(limit=stop-start, offset=start)

    @classmethod
    def save_item(cls, item):
        if not item.need_update:
            return False
        declare = []
        params = {}
        added = []
        for field in item.params:
            field = item.params[field]
            if field.need_update:
                field.changed = False
                added.append(field.name)
                params[f'${field.name}'] = field.to_save
                declare.append(f"DECLARE ${field.name} AS {field.title};")

        sql = f'''UPSERT INTO {item.table_name}
        ({', '.join([f'`{field}`' for field in added])})
        VALUES ({', '.join([f'${field}' for field in added])})'''
        if declare:
            sql = '\n'.join(declare) + '\n' + sql
        item._database_.query(sql, params)
        return True


class QueryResult:
    def __init__(self, query, limit, offset, lazy):
        self._query = query
        self._limit = limit
        self._offset = offset
        self._items = None if lazy else self._query._actual_fetch(limit, offset)

    def __len__(self):
        if self._items is None:
            self._items = self._query._actual_fetch(self._limit, self._offset)
        return len(self._items)

    def __getitem__(self, item):
        return self._items[item]