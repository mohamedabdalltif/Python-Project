# import libraries

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# read file 

df=pd.read_csv("Summer22_FootballTransfers.csv",delimiter=";",decimal=',' ,encoding='latin1')
# print(df.head())

# ---------------------------------------------------------------------------------- #
# cleaning NaN


df=df.dropna()

# ---------------------------------------------------------------------------------- #
# cleaning foreign chars

import re
def replace_foreign_characters(s):
    return re.sub(r'[^\x00-\x7f]',r'', s)

for i in df.columns:
    
    if i=='cost' or i=='age':
        continue
    
    df[i]= df[i].apply(lambda x: replace_foreign_characters(x))



# ---------------------------------------------------------------------------------- #
# cost col  to numeric

df1=df.cost.str.extract('(?P<columnA>.{3})(?P<columnB>.{1,})')
result = df1['columnB'].str.split('(\d+)([A-Za-z]+)', expand=True)
result = result.loc[:,[0,1,2]]
result.rename(columns={0:'x', 1:'y',2:'z'}, inplace=True)
result['x'] = pd.to_numeric(result['x'].astype(str) +""+ result["y"],errors='coerce') 
result.loc[result['z']=='m','x']=result[result['z']=='m'][result.select_dtypes(include=['float64']).columns]*1000000
result.loc[result['z']=='Th','x']=result[result['z']=='Th'][result.select_dtypes(include=['float64']).columns]*1000

df['cost']=result['x']


print(df['cost'])


# ---------------------------------------------------------------------------------- #
# important values

position_categories=set(df['position'])
new_clubs=set(df['new_club'])
origin_clubs=set(df['origin_club'])
age_categories=set(df['age'])
league_origin_categories=set(df['league_origin_club'])
league_new_categories=set(df['league_new_club'])

print(position_categories)


# ---------------------------------------------------------------------------------- #
# most purchased postision


postision_count = df.groupby(['position'])['position'].count().to_frame()
postision_count=postision_count.rename(columns={"position": "count"}).sort_values(by=["count"],ascending=False)

ax = plt.axes()

postision_count.plot.bar(y='count',color='r',title='most purchased postision')

print(postision_count['count'])

# ---------------------------------------------------------------------------------- #
# most demanded age 

age_count = df.groupby(['age'])['age'].count().to_frame()
age_count=age_count.rename(columns={"age": "count"}).sort_values(by=["count"],ascending=False)

ax = plt.axes()

age_count.plot.bar(y='count',color='g',title='most demanded age ')




# print(postision_count['count'])








