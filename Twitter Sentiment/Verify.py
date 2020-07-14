import numpy as np
import sqlalchemy as db
import pandas as pd
engine=db.create_engine('mysql://u831388458_covid19:Password@123@34.89.97.3:3306/u831388458_covid19stats',pool_recycle=1)
tablist=[]
for (tname,) in engine.execute('SHOW TABLES'):
    tablist.append(tname)
writer=pd.ExcelWriter('50 Hands/USA/RData.xlsx',engine='xlsxwriter')
for i in tablist:
    if 'twitter_nlp' in i:
        df=pd.read_sql_table(i,engine)
l=df['polarity_score'].tolist()
print(np.var(l))
print(np.std(l))
l=[i+2 for i in l]
l=[(9*(i-1)/2)+1 for i in l]
print(np.var(l))
print(np.std(l))
