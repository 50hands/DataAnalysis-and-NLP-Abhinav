import pandas as pd
df=pd.read_excel('50 Hands/USA/USAStateData.xlsx',sheet_name='Sheet1')
for i in range(len(df)):
    s=str(df.loc[i,'case_per_100000']).split(' ')
    df.loc[i,'case_per_100000']=float(s[0])
writer=pd.ExcelWriter('50 Hands/USA/USAStateData.xlsx',engine='xlsxwriter')
df.to_excel(writer,sheet_name='Sheet1',index=False)
writer.save()
