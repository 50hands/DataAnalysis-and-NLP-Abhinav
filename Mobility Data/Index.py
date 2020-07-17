import pandas as pd
import numpy as np
from datetime import datetime
import sqlalchemy as db
df=pd.read_csv('https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_confirmed_usafacts.csv')
df=df.melt(id_vars=['countyFIPS','County Name','State','stateFIPS'],var_name="date",value_name="case")
df['date']=df['date'].map(lambda x:str(datetime.strptime(str(x),'%m/%d/%y')).split(' ')[0])
df['date']=df['date'].map(lambda x:x.split('-')[2]+'-'+x.split('-')[1]+'-'+x.split('-')[0])
countycasedata=df
engine=db.create_engine('mysql://u831388458_covid19:Password@123@34.89.97.3:3306/u831388458_covid19stats',pool_recycle=1)
tablist=[]
for (tname,) in engine.execute('SHOW TABLES'):
    tablist.append(tname)
df=pd.DataFrame()
for i in tablist:
    if 'mobility' in i and 'Ind' not in i:
        tdf=pd.read_sql_table(i,engine)
        df=df.append(tdf,ignore_index=True)
    if i=='case_history_by_province':
        canadadata=pd.read_sql_table(i,engine)
        l=['date_report','province_id']
        canadadata=canadadata.drop_duplicates(subset=l,keep="last")
        canadadata=canadadata[['date_report','provincial_case_id','province_id']]
        canadadata.insert(3,'country_region','Canada')
        canadadata.insert(4,'sub_region_2','(Base Level)')
    if i=='provinces':
        canadapcode=pd.read_sql_table(i,engine)
        canadapcode=canadapcode[['province_id','province_name','province_population']]
        canadapop=canadapcode[['province_name','province_population']]
        canadapop=canadapop.rename(columns={"province_population":"population","province_name":"sub_region_1"})
        canadapop.insert(2,'country_region','Canada')
        canadapop.insert(3,'sub_region_2','(Base Level)')
    if i=='US_covid_trend_state_lvl':
        usadata=pd.read_sql_table(i,engine)
        l=['Province_State','Country_Region','Last_Update','Confirmed']
        usadata=usadata[l]
        usadata=usadata.rename(columns={"Province_State":"sub_region_1","Country_Region":"country_region","Last_Update":"date","Confirmed":"case"})
        usadata=usadata.replace(to_replace='US',value='United States')
        usadata.insert(4,'sub_region_2','(Base Level)')
    if i=='US_state_population':
        usapop=pd.read_sql_table(i,engine)
        usapop=usapop[['state_name','total']]
        usapop=usapop.rename(columns={"state_name":"sub_region_1","total":"population"})
        usapop.insert(2,'country_region','United States')
        usapop.insert(3,'sub_region_2','(Base Level)')
    if i=='US_Geo_Location':
        usapcode=pd.read_sql_table(i,engine)
        usapcode=usapcode.rename(columns={"State_ID":"State"})
    if i=='US_county_population':
        countypop=pd.read_sql_table(i,engine)
        l=['state_name','county_name','total_population']
        countypop=countypop[l]
        countypop=countypop.rename(columns={"total_population":"population","county_name":"sub_region_2","state_name":"sub_region_1"})
        countypop.insert(3,'country_region','United States')
pop=pd.DataFrame()
pop=pop.append(canadapop,ignore_index=True)
pop=pop.append(usapop,ignore_index=True)
pop=pop.append(countypop,ignore_index=True)
countycasedata=pd.merge(countycasedata,usapcode,how='left',left_on='State',right_on='State')
l=['County Name','date','case','State_Name']
countycasedata=countycasedata[l]
countycasedata.insert(4,'country_region','United States')
countycasedata=countycasedata.rename(columns={"State_Name":"sub_region_1","County Name":"sub_region_2"})
usadata['date']=usadata['date'].map(lambda x:x.split(' ')[0])
usadata=usadata[usadata['date']!='']
usadata['date']=usadata['date'].map(lambda x:x.split('-')[2]+'-'+x.split('-')[1]+'-'+x.split('-')[0])
canadadata=pd.merge(canadadata,canadapcode,how='left',left_on='province_id',right_on='province_id')
canadadata=canadadata[['date_report','provincial_case_id','country_region','sub_region_2','province_name']]
canadadata=canadadata.rename(columns={"date_report":"date","provincial_case_id":"case","province_name":"sub_region_1"})
usadata=usadata.append(canadadata,ignore_index=True)
casedata=usadata
casedata=casedata.append(countycasedata,ignore_index=True)
l=['country_region','sub_region_1','sub_region_2','date','retail_and_recreation_percent_change_from_baseline','grocery_and_pharmacy_percent_change_from_baseline','parks_percent_change_from_baseline','transit_stations_percent_change_from_baseline','workplaces_percent_change_from_baseline','residential_percent_change_from_baseline']
df[['sub_region_1','sub_region_2']]=df[['sub_region_1','sub_region_2']].replace(to_replace='',value='(Base Level)')
df=df.fillna(0)
df=df[l]
df=df.replace(to_replace='',value='0')
times=list(pd.date_range('15-02-2020',periods=147,freq='1440min').strftime("%d-%m-%Y"))
l=['country_region','sub_region_1','sub_region_2']
df3=df[l]
df3=df3.drop_duplicates(subset=l,keep="last").reset_index()
df2=pd.DataFrame()
for i in range(len(df3)):
    d={'country_region':df3.loc[i,'country_region'],'sub_region_1':df3.loc[i,'sub_region_1'],'sub_region_2':df3.loc[i,'sub_region_2'],'date':times}
    df_flag=pd.DataFrame(d)
    df2=df2.append(df_flag,ignore_index=True)
df['date']=df['date'].map(lambda x:x.split('-')[2]+'-'+x.split('-')[1]+'-'+x.split('-')[0])
df2=pd.merge(df2,df,how='left',left_on=['country_region','sub_region_1','sub_region_2','date'],right_on=['country_region','sub_region_1','sub_region_2','date'])
df2=df2.fillna(0)
df2=df2.replace(to_replace='',value='0')
df2=df2.replace(to_replace=' ',value='0')
df=pd.merge(df2,casedata,how='left',left_on=['country_region','sub_region_1','sub_region_2','date'],right_on=['country_region','sub_region_1','sub_region_2','date'])
df=df.fillna(0)
df=df.replace(to_replace='',value='0')
df=df.replace(to_replace=' ',value='0')
for i in range(1,len(df)):
    if df.loc[i,'case']==0 and str(df.loc[i,'country_region'])==str(df.loc[i-1,'country_region']) and str(df.loc[i,'sub_region_1'])==str(df.loc[i-1,'sub_region_1']) and str(df.loc[i,'sub_region_2'])==str(df.loc[i-1,'sub_region_2']):
        df.loc[i,'case']=df.loc[i-1,'case']
df=pd.merge(df,pop,how='left',left_on=['country_region','sub_region_1','sub_region_2'],right_on=['country_region','sub_region_1','sub_region_2'])
df=df.fillna(0)
df=df.replace(to_replace='',value='0')
df=df.replace(to_replace=' ',value='0')
writer=pd.ExcelWriter('GoogleMobilityData2.xlsx',engine='xlsxwriter')
df.to_excel(writer,sheet_name='Sheet1',index=False)
writer.save()
