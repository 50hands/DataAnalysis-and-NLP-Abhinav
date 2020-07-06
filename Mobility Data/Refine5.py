import numpy as np
import pandas as pd
times=list(pd.date_range('15-02-2020',periods=126,freq='1440min').strftime("%d-%m-%Y"))
df=pd.read_excel('50 Hands/Mobility Data/GoogleMobilityData.xlsx',sheet_name='Sheet1')
print('Extracted')
l=['country_region','sub_region_1','sub_region_2']
df3=df[l]
df3=df3.drop_duplicates(subset=l,keep="last").reset_index()
d={'country_region':[0],'sub_region_1':[0],'sub_region_2':[0],'date':[0]}
df2=pd.DataFrame(d)
temp=0
print('Formed')
for i in range(len(df3)):
    s1=df3.loc[i,'country_region']
    s2=df3.loc[i,'sub_region_1']
    s3=df3.loc[i,'sub_region_2']
    for j in times:
        df2.loc[temp,'country_region']=s1
        df2.loc[temp,'sub_region_1']=s2
        df2.loc[temp,'sub_region_2']=s3
        df2.loc[temp,'date']=j
        temp+=1
print('Processed 1')
df2=pd.merge(df2,df,how='left',left_on=['country_region','sub_region_1','sub_region_2','date'],right_on=['country_region','sub_region_1','sub_region_2','date'])
print('Merged')
writer=pd.ExcelWriter('50 Hands/Mobility Data/GoogleMobilityData.xlsx',engine='xlsxwriter')
df.to_excel(writer,sheet_name='Sheet1',index=False)
writer.save()
