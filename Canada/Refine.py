import pandas as pd
df=pd.read_excel('50 Hands/Poo.xlsx',sheet_name='case_history_by_province')
df2=pd.read_excel('50 Hands/Poo.xlsx',sheet_name='countries')
df3=pd.read_excel('50 Hands/Poo.xlsx',sheet_name='provinces')
df4=pd.read_excel('50 Hands/Poo.xlsx',sheet_name='health_regions')
print('Done loading Databases!!')
df=pd.merge(df,df2,how='left',left_on='country_id',right_on='country_id')
df=pd.merge(df,df3,how='left',left_on='province_id',right_on='province_id')
df=pd.merge(df,df4,how='left',left_on='health_region',right_on='health_region')
print('Done merging!!')
df['locally_acquired']=df['locally_acquired'].fillna('Mode of acquirement unknown')
for i in range(len(df)):
    if df.loc[i,'travel_yn']=='Not Reported':
        df.loc[i,'travel_history_country']='Travel Data Unavailable'
df['travel_history_country']=df['travel_history_country'].fillna('No Travel History')
print('Phase 1 of data cleaning done!!')
origcol=['case_id','age_range','date_report','gender','health_region','locally_acquired','provincial_case_id','report_week','travel_history_country','latitude_x','longitude_x','country_name','latitude_y','longitude_y','province_name','latitude', 'longitude']
df=df[origcol]
df=df.rename(columns={'latitude_x':'Latitude_can','longitude_x':'Longitude_can','latitude_y':'Latitude_pro','longitude_y':'Longitude_pro','latitude':'Latitude_hco','longitude':'Longitude_hco'})
df.drop_duplicates(subset="case_id",keep='last',inplace=True)
print('Final cleaning done!!')
'''writer=pd.ExcelWriter('50 Hands/CovidData.xlsx',engine='xlsxwriter')
df.to_excel(writer,sheet_name='Sheet1')
writer.save()'''
