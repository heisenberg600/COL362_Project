import pandas as pd
df = pd.read_csv('reviews.csv')
for index,row in df.iterrows():
	if (row['restId']==0):
		df.at[index,'restId']=1


for index,row in df.iterrows():
	if (row['restId']==0):
		print('yes)')
		
		
df.to_csv('r.csv',index=False)	
