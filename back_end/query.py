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

        self.execute(query)
        self.cols = [desc[0] for desc in self.cursor.description]
        
        ans = self.cursor.fetchall()

        self.s.add((query, time.time()-start))

        return ans

    def insert(self, table, values:list):
        values = ', '.join(values)
        query = f'insert into {table} values({values})'

        start = time.time()
        self.execute(query)
        self.s.add((query, time.time()-start))

    def update(self, table, data, cond):
        upd = []
        for i in data:
            curr = str(i) + " = "
            val = data[i]
            if(type(val) == str):
                curr += f"'{data[i]}'"
            else:
                curr += str(data[i])
            upd.append(curr)
        query = f'update {table} set {", ".join(upd)} where {cond}'

        start = time.time()
        self.execute(query)
        self.s.add((query, time.time()-start))

    def dump(self):
        file = open('queries.txt','w')
        for i in self.s:
            print(i)
            file.write(i[0] + ': ' + str(i[1]) + '\n')

