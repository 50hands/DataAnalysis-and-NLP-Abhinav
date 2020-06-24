import sqlalchemy as db
import pandas as pd
engine=db.create_engine('mysql://u831388458_covid19:Password@123@213.190.6.106:3306/u831388458_covid19stats',pool_recycle=1)
tablist=[]
tablist2=[]
writer=pd.ExcelWriter('50 Hands/USA/Poo.xlsx',engine='xlsxwriter')
for (tname,) in engine.execute('SHOW TABLES'):
    tablist.append(tname)
for i in tablist:
    if 'US' in i or i=='ca_google_mobility_data':
        res=engine.execute('SELECT COUNT(*) FROM '+i)
        x=res.fetchall()[0][0]
        if x>0:
            print(i,x)
            df=pd.read_sql_table(i,engine)
            df.to_excel(writer,sheet_name=i[:30])
writer.save()
df=pd.read_sql_table('US_pop_density_states',engine)
writer=pd.ExcelWriter('50 Hands/USA/USADensityData.xlsx',engine='xlsxwriter')
df.to_excel(writer,sheet_name='Sheet1',index=False)
writer.save()
