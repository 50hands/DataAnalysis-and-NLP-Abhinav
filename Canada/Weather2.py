from wwo_hist import retrieve_hist_data
import os
import urllib.request
import numpy as np
import pandas as pd
import datetime
os.chdir("./50 Hands")
frequency=24
start_date='25-JAN-2020'
end_date='18-MAY-2020'
api_key=''
location_list=['Abitibi-Temiscamingue','Algoma','Bas-Saint-Laurent','Brant','Cote-Nord','Calgary','Capitale-Nationale','Central','Chatham-Kent','Chaudiere-Appalaches','Durham','Eastern','Edmonton','Far-North','Fraser','Gaspesie-Iles-de-la-Madeleine','Grey-Bruce','Haliburton-Kawartha-Pine-Ridge','Haldimand-County', 'Halton', 'Hamilton','Hastings-Prince-Edward', 'Huron-Perth', 'Interior','Interlake-Eastern','Island','Kingston-Frontenac-Lennox-&-Addington','Labrador-Grenfell','Lambton','Laurentides','Laval','Leeds-Grenville-and-Lanark','Mauricie','Middlesex-London','Montreal','Niagara','Nord-du-Quebec','North','North-Bay-Parry-Sound','Northern','Northwestern','Nunavut','NWT','Ottawa','Peel','Peterborough','Porcupine','Prairie-Mountain','Prince-Edward-Island','Regina','Renfrew','Saguenay','Saskatoon','Simcoe-Muskoka','South','Southern-Health','Southwestern','Sudbury','Terres-Cries-de-la-Baie-James','Thunder-Bay','Timiskaming','Toronto','Vancouver Coastal','Waterloo','Wellington-Dufferin-Guelph','Western','Windsor-Essex','Winnipeg','York','Yukon','Bathurst-Area','Miramichi-Area','Campbellton-Area','Edmundston-Area','Fredericton-Area','Saint-John-Area','Moncton-Area']
'''hist_weather_data=retrieve_hist_data(api_key,location_list,start_date,end_date,frequency,location_label=False,export_csv=True,store_df=True)'''
df=pd.DataFrame()
for i in location_list:
    s='50 Hands/'+i+'.csv'
    df1=pd.read_csv(s)
    l=[i for j in range(len(df1))]
    df1.insert(0,'health_region',l)
    df1=df1[['health_region','date_time','tempC','humidity']]
    df=df.append(df1,ignore_index=True)
for i in range(len(df)):
    s=df.loc[i,'date_time'].split('-')
    df.loc[i,'date_time']=s[2]+'-'+s[1]+'-'+s[0]
df=df.rename(columns={'date_time':'date_report'})
writer=pd.ExcelWriter('50 Hands/CovidDataWeatherHistoryRegion.xlsx',engine='xlsxwriter')
df.to_excel(writer,sheet_name='Sheet1')
writer.save()
for i in location_list:
    s='50 Hands/'+i+'.csv'
    os.remove(s)
