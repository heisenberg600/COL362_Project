import time


class Query:
    def __init__(self, cursor):
        self.cursor = cursor
        self.execute = cursor.execute
        self.s = set()
        self.cols = []

    def select(self, attr:list, tables:list, condition:str = '', order:list = [], group:list = [], limit = -1, distinct = False):

        select = 'select'
        if(distinct): select = 'select distinct'

        if(order == []): order = ''
        else: order = 'order by ' + ', '.join(order)

        if(group == []): group = ''
        else: group = 'group by ' + ', '.join(group)

        if(condition == ''): condition = ''
        else: condition = 'where ' + condition

        if(limit < 0):limit = ''
        else: limit = f'limit {limit}'

        tables = ', '.join(tables)
        attr = ', '.join(attr)

        start = time.time()
        
        query = f'{select} {attr} from {tables} {condition} {group} {order} {limit}'
        print(query)
        self.execute(query)
        self.cols = [desc[0] for desc in self.cursor.description]
        
        ans = self.cursor.fetchall()

        self.s.add(query)

        return ans

    def insert(self, table, values:list):
        start = time.time()
        values = ', '.join(values)
        query = f'insert into {table} values({values})'
        self.execute(query)
        self.s.add(query)


    def dump(self):
        file = open('queries.txt','w')
        for i in self.s:
            file.write(i[0] + ': ' + str(i[1]) + '\n')
        file.close()
