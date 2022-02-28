class Query:
    def __init(self, cursor):
        self.cursor = cursor
        self.execute = cursor.execute
    
    def select(self, attr:list, tables:list, condition:str = '', order:list = [], group:list = [], distinct = False):

        select = 'select'
        if(distinct): select = 'select distinct'

        if(order == []): order = ''
        else: order = 'order by ' + ', '.join(order)

        if(group == []): group = ''
        else: group = 'group by ' + ', '.join(group)

        if(condition == ''): condition = ''
        else: condition = 'where ' + condition

        tables = ', '.join(tables)
        attr = ', '.join(attr)
    
        self.execute(f'{select} {attr} from {tables} {condition} {group} {order}')
        return self.cursor.fetchall()

    def insert(self, table, values:list):
        self.execute(f'insert into {table} values {values}')
