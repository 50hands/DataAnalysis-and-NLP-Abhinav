import pandas as pd
df=pd.read_excel('50 Hands/India/Poo.xlsx',sheet_name='Ind_national_lvl_recent_upd')
for i in range(len(df)):
    s=df.loc[i,'date'].split(' ')
    if s[1]=='January':
        df.loc[i,'date']=s[0]+'-01-2020'
    elif s[1]=='February':
        df.loc[i,'date']=s[0]+'-02-2020'
    elif s[1]=='March':
        df.loc[i,'date']=s[0]+'-03-2020'
    elif s[1]=='April':
        df.loc[i,'date']=s[0]+'-04-2020'
    elif s[1]=='May':
        df.loc[i,'date']=s[0]+'-05-2020'
    elif s[1]=='June':
        df.loc[i,'date']=s[0]+'-06-2020'
writer=pd.ExcelWriter('50 Hands/India/CovidDataCases.xlsx',engine='xlsxwriter')
df.to_excel(writer,sheet_name='Sheet1')
writer.save()
