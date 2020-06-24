import sqlalchemy as db
import pandas as pd
df=pd.read_excel('50 Hands/USA/USAStateData.xlsx',sheet_name='Sheet1')
df1=pd.read_excel('50 Hands/USA/USADensityData.xlsx',sheet_name='Sheet1')
df=pd.merge(df,df1,how='left',left_on='state_name',right_on='state_name')
df=df.fillna(0)
writer=pd.ExcelWriter('50 Hands/USA/USAStateData2.xlsx',engine='xlsxwriter')
df.to_excel(writer,sheet_name='Sheet1',index=False)
writer.save()
