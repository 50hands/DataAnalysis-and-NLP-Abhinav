import pandas as pd
df=pd.read_excel('50 Hands/Mobility Data/GoogleMobilityData.xlsx',sheet_name='Sheet1')
df=df.fillna(0)
for i in range(1,len(df)):
    if df.loc[i,'case']==0 and str(df.loc[i,'country_region'])==str(df.loc[i-1,'country_region']) and str(df.loc[i,'sub_region_1'])==str(df.loc[i-1,'sub_region_1']) and str(df.loc[i,'sub_region_2'])==str(df.loc[i-1,'sub_region_2']):
        df.loc[i,'case']=df.loc[i-1,'case']
writer=pd.ExcelWriter('50 Hands/Mobility Data/GoogleMobilityData.xlsx',engine='xlsxwriter')
df.to_excel(writer,sheet_name='Sheet1',index=False)
writer.save()
