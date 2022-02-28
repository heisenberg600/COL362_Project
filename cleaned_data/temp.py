import pandas as pd
import random
df = pd.read_csv('reviews.csv')

list=random.sample([i for i in range(1,len(df))],20000)

trunc=[]
for row in list:
	trunc.append(df.iloc[row])
reviews=pd.DataFrame(trunc,columns=['userId','restId','stars'])
reviews.to_csv('r.csv',index=False)
