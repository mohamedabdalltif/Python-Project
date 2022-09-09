# import libraries

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from warnings import filterwarnings
filterwarnings("ignore")


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

df.cost = df["cost"].str.replace("ýýý","")

def value_to_float(x):
    if type(x) == float or type(x) == int:
        return x
    if 'Th' in x:
        if len(x) > 1:
            return float(x.replace('Th', '')) * 1000
        return 1000.0
    if 'm' in x:
        if len(x) > 1:
            return float(x.replace('m', '')) * 1000000
        return 1000000.0
    return 0.0

df['cost'] = df['cost'].apply(value_to_float)

# print(df.head())

# print(df['cost'])


# ---------------------------------------------------------------------------------- #
# important values

# position_categories=set(df['position'])
# new_clubs=set(df['new_club'])
# origin_clubs=set(df['origin_club'])
# age_categories=set(df['age'])
# league_origin_categories=set(df['league_origin_club'])
# league_new_categories=set(df['league_new_club'])

# print(position_categories)


# ---------------------------------------------------------------------------------- #
# most purchased postision
# ax = plt.axes()

postision_count = df.groupby(['position'])['position'].count().to_frame()
postision_count=postision_count.rename(columns={"position": "count"}).sort_values(by=["count"],ascending=False)



postision_count.plot.bar(y='count',color='r',title='most purchased postision')
plt.show()
# print(postision_count['count'])

# ---------------------------------------------------------------------------------- #
# most demanded age 

age_count = df.groupby(['age'])['age'].count().to_frame()
age_count=age_count.rename(columns={"age": "count"}).sort_values(by=["count"],ascending=False)
age_count.plot.bar(y='count',color='g',title='most demanded age ')
plt.show()




# print(postision_count['count'])





# print the most country

df.groupby('league_new_club').league_new_club.count()

## ordering the frequencies ##
df.groupby('league_new_club').league_new_club.count().sort_values(ascending=False)


## although, this .agg() function transforms all the data to the group frequency of "league_new_club", we can still use
## it to locate the most the leagues with the most transfers 
leagues_by_len = df.groupby(['league_new_club']).agg([len])
leagues_by_len.head()

## only leagues with above 250 transfers 
league_filter = leagues_by_len.loc[(leagues_by_len.league_origin_club.len >= 250) & (leagues_by_len.league_origin_club.len <= 800)]
## also including a upper boundary to exlucde the Italy league, as this is likely a cumulation of all the Series Leagues


## In this visualization we will look for rankings of the leagues to.
sns.countplot(df[:20].league_new_club)
plt.xlabel("League Names",fontsize=12)
plt.ylabel("Count",fontsize=12)
plt.show()

## Transfers To 
labels = df[:20].league_new_club.value_counts().index

colors = ["blue","red","green","yellow"]

sizes = df[:20].league_new_club.value_counts().values
explode = np.zeros(len(sizes))
plt.figure(figsize = (7,7))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%')
plt.title('Transfers Leagues to',color = 'blue',fontsize = 15)
plt.show()

















































