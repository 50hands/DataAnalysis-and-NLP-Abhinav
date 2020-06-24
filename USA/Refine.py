import pandas as pd
df=pd.read_excel('50 Hands/USA/Poo.xlsx',sheet_name='US_JHU_state_level_data')
df1=pd.read_excel('50 Hands/USA/Poo.xlsx',sheet_name='US_cancer_state')
df2=pd.read_excel('50 Hands/USA/Poo.xlsx',sheet_name='US_race_state')
df=pd.merge(df,df1,how='left',left_on='state_name',right_on='state_name')
df=pd.merge(df,df2,how='left',left_on='state_name',right_on='state_name')
for i in range(len(df)):
    for j in range(len(df.columns)):
        if df.iloc[i,j]==' ':
            df.iloc[i,j]=0
        if '<' in str(df.iloc[i,j]):
            s=df.iloc[i,j]
            df.iloc[i,j]='0'+s[1:]
            df.iloc[i,j]=float(df.iloc[i,j])
df3=pd.read_excel('50 Hands/USA/Poo.xlsx',sheet_name='US_diabetes_state_level')
l=['Year','state_name','Percentage']
df3=df3[l]
df4=df3[df3['Year']==2015]
df5=df3[df3['Year']==2016]
df=pd.merge(df,df4,how='left',left_on='state_name',right_on='state_name')
df=pd.merge(df,df5,how='left',left_on='state_name',right_on='state_name')
df6=pd.read_excel('50 Hands/USA/Poo.xlsx',sheet_name='US_drug_state')
df7=df6[df6['Drug_type']=='Marijuana']
df8=df6[df6['Drug_type']=='Cocaine']
df9=df6[df6['Drug_type']=='Heroin']
df10=df6[df6['Drug_type']=='Methamphetamine']
df11=df6[df6['Drug_type']=='Illicit drug']
df=pd.merge(df,df7,how='left',left_on='state_name',right_on='state_name')
df=pd.merge(df,df8,how='left',left_on='state_name',right_on='state_name')
df=pd.merge(df,df9,how='left',left_on='state_name',right_on='state_name')
df=pd.merge(df,df10,how='left',left_on='state_name',right_on='state_name')
df=pd.merge(df,df11,how='left',left_on='state_name',right_on='state_name')
df=df.fillna(0)
writer=pd.ExcelWriter('50 Hands/USA/USAStateData.xlsx',engine='xlsxwriter')
df.to_excel(writer,sheet_name='Sheet1',index=False)
writer.save()
