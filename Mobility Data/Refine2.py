import pandas as pd
writer=pd.ExcelWriter('50 Hands/Mobility Data/HistoricalData.xlsx',engine='xlsxwriter')
df=pd.read_excel('50 Hands/Mobility Data/HistoryData.xlsx',sheet_name='US_CTP_state_historical_data')
df2=pd.read_excel('50 Hands/Mobility Data/HistoryData.xlsx',sheet_name='USA_Geolocation_Data')
df=df[['state','date','positive']]
df.insert(3,'Country','United States')
df.insert(4,'sub_region_2','(Base Level)')
for i in range(len(df)):
    s=str(df.loc[i,'date'])
    df.loc[i,'date']=s[6:]+'-'+s[4:6]+'-'+s[0:4]
df=pd.merge(df,df2,how='left',left_on='state',right_on='state')
df.to_excel(writer,sheet_name='USA',index=False)
df=pd.read_excel('50 Hands/Mobility Data/HistoryData.xlsx',sheet_name='case_history_by_province')
l=['date_report','province_id']
df=df.drop_duplicates(subset=l,keep="last")
df2=pd.read_excel('50 Hands/Mobility Data/HistoryData.xlsx',sheet_name='CanadaPCode')
df=df[['case_id','date_report','provincial_case_id','province_id']]
df.insert(4,'Country','Canada')
df.insert(5,'sub_region_2','(Base Level)')
df=pd.merge(df,df2,how='left',left_on='province_id',right_on='province_id')
df.to_excel(writer,sheet_name='Canada',index=False)
df=pd.read_excel('50 Hands/USA/Poo.xlsx',sheet_name='US_covid_trend_county_lvl')
df=df[['County_name','Province_State','Country_Region','Last_Update','Lat','Lon','Confirmed']]
df=df.fillna(0)
for i in range(len(df)):
    if df.loc[i,'County_name']!=0:
        df.loc[i,'County_name']=df.loc[i,'County_name']+' County'
        if df.loc[i,'Country_Region']=='US':
            df.loc[i,'Country_Region']='United States'
        if '-' in str(df.loc[i,'Last_Update']):
            s=str(df.loc[i,'Last_Update']).split(' ')[0].split('-')
            df.loc[i,'Last_Update']=s[2]+'-'+s[1]+'-'+s[0]
        elif '/' in str(df.loc[i,'Last_Update']):
            s=str(df.loc[i,'Last_Update']).split(' ')[0].split('/')
            df.loc[i,'Last_Update']=s[1]+'-'+s[0]+'-2020'
df=df.rename(columns={"County_name":"sub_region_2","Province_State":"sub_region_1","Country_Region":"country_region","Last_Update":"date","Lat":"latitude","Lon":"Longitude","Confirmed":"case"})
df.to_excel(writer,sheet_name='USACounty',index=False)
writer.save()
