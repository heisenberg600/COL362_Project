import time


class Query:
    def __init(self, cursor):
        self.cursor = cursor
        self.execute = cursor.execute
        self.s = set()
    
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

        start = time.time()
        
        query = f'{select} {attr} from {tables} {condition} {group} {order}'
        self.execute(query)
        ans = self.cursor.fetchall()

        self.s.add(query,time.time()-start)

        return ans

    def insert(self, table, values:list):
        self.execute(f'insert into {table} values {values}')

    def dump(self):
        file = open('queries.txt','w')
        for i in self.s:
            file.write(i[0] + ': ' + str(i[1]) + '\n')
        file.close()
