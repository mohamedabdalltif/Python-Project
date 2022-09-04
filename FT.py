# import libraries

import pandas as pd

import numpy as np



# read file 

df=pd.read_csv("Summer22_FootballTransfers.csv",delimiter=";",decimal=',' ,encoding='latin1')

# print(df.head())


# cost col  to numeric

df1=df.cost.str.extract('(?P<columnA>.{3})(?P<columnB>.{1,})')
result = df1['columnB'].str.split('(\d+)([A-Za-z]+)', expand=True)
result = result.loc[:,[0,1,2]]
result.rename(columns={0:'x', 1:'y',2:'z'}, inplace=True)
result['x'] = pd.to_numeric(result['x'].astype(str) +""+ result["y"],errors='coerce') 

result.loc[result['z']=='m','x']=result[result['z']=='m'][result.select_dtypes(include=['float64']).columns]*1000000
result.loc[result['z']=='Th','x']=result[result['z']=='Th'][result.select_dtypes(include=['float64']).columns]*1000

df['cost']=result['x']


#cleaning NaN


df=df.dropna()



#important values

position_categories=set(df['position'])
new_clubs=set(df['new_club'])
origin_clubs=set(df['origin_club'])
age_categories=set(df['age'])
league_origin_categories=set(df['league_origin_club'])
league_new_categories=set(df['league_new_club'])

print(len(league_new_categories))




