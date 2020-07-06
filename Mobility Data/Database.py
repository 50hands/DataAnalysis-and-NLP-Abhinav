import sqlalchemy as db
import pandas as pd
engine=db.create_engine('mysql://u831388458_covid19:Password@123@213.190.6.106:3306/u831388458_covid19stats',pool_recycle=1)
tablist=[]
for (tname,) in engine.execute('SHOW TABLES'):
    tablist.append(tname)
writer=pd.ExcelWriter('50 Hands/Mobility Data/HistoryData.xlsx',engine='xlsxwriter')
for i in tablist:
    if 'hist' in i:
        print(i)
        df=pd.read_sql_table(i,engine)
        df.to_excel(writer,sheet_name=i[:30])
writer.save()
