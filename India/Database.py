import sqlalchemy as db
import pandas as pd
engine=db.create_engine('mysql://u831388458_covid19:Password@123@213.190.6.106:3306/u831388458_covid19stats',pool_recycle=1)
tablist=[]
writer=pd.ExcelWriter('50 Hands/India/Poo.xlsx', engine='xlsxwriter')
for (tname,) in engine.execute('SHOW TABLES'):
    tablist.append(tname)
print(tablist)
'''for i in tablist:
    if 'Ind' in i:
        res=engine.execute('SELECT COUNT(*) FROM '+i)
        x=res.fetchall()[0][0]
        if x>0:
            print(i,x)
            df=pd.read_sql_table(i,engine)
            df.to_excel(writer,sheet_name=i[:30])
writer.save()'''
