import pandas as pd
import random
df = pd.read_csv('reviews.csv')


df_2=pd.read_csv('ra.csv')

avgreview=[0 for i in range(len(df_2))]
numreview=[0 for i in range(len(df_2))]

for index, rows in df.iterrows():
	avgreview[rows['restId']-1]=(avgreview[rows['restId']-1]*numreview[rows['restId']-1]+rows['stars'])/(numreview[rows['restId']-1]+1)
	numreview[rows['restId']-1]+=1

print(len(avgreview))
print(len(numreview))

df_2['avgReview']=list(map(lambda x: round(x,2),avgreview))
df_2['num_reviews']=numreview

print(df_2)
df_2.to_csv('restaurants.csv',index=False)
