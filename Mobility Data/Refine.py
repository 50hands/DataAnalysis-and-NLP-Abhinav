import pandas as pd
df=pd.read_excel('50 Hands/DensityData.xlsx',sheet_name='Ind_google_mobility')
df=df.fillna({'sub_region_1':'(Base Level)','sub_region_2':'(Base Level)'})
df=df.fillna(0)
df2=pd.read_excel('50 Hands/DensityData.xlsx',sheet_name='ca_google_mobility')
df2=df2.fillna({'sub_region_1':'(Base Level)','sub_region_2':'(Base Level)'})
df2=df2.fillna(0)
df3=pd.read_excel('50 Hands/USADensityData.xlsx',sheet_name='US_google_mobility')
df3=df3.fillna({'sub_region_1':'(Base Level)','sub_region_2':'(Base Level)'})
df3=df3.fillna(0)
df=df.append(df2,ignore_index=True)
df=df.append(df3,ignore_index=True)
for i in range(len(df)):
    s=str(df.loc[i,'date']).split('-')
    df.loc[i,'date']=s[2]+'-'+s[1]+'-'+s[0]
writer=pd.ExcelWriter('50 Hands/GoogleMobility.xlsx',engine='xlsxwriter')
df.to_excel(writer,sheet_name='Sheet1',index=False)
writer.save()
