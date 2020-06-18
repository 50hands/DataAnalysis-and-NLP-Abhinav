import pandas as pd
df=pd.read_csv('Provincial_Daily_Totals.csv')
for i in range(len(df)):
    s=df.loc[i,'SummaryDate'].split(' ')[0]
    s=s.split('/')
    s=s[2]+'-'+s[1]+'-'+s[0]
    df.loc[i,'SummaryDate']=s
df=df.fillna(0)
writer=pd.ExcelWriter('50 Hands/Canada/CovidDataCriticalCases.xlsx',engine='xlsxwriter')
df.to_excel(writer,sheet_name='Sheet1')
writer.save()
