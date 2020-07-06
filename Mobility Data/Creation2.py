import pandas as pd
from datetime import datetime
df=pd.read_csv('https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_confirmed_usafacts.csv')
df=df.melt(id_vars=['countyFIPS','County Name','State','stateFIPS'],var_name="date",value_name="case")
for i in range(len(df)):
    a=datetime.strptime(str(df.loc[i,'date']),'%m/%d/%y')
    a=str(a).split(' ')[0]
    a=a.split('-')
    df.loc[i,'date']=a[2]+'-'+a[1]+'-'+a[0]
df=df.sort_values(by=['State','County Name']).reset_index()
df=df[['State','County Name','date','case']]
writer=pd.ExcelWriter('50 Hands/Mobility Data/CountyData.xlsx',engine='xlsxwriter')
df.to_excel(writer,sheet_name='Sheet1',index=False)
writer.save()
