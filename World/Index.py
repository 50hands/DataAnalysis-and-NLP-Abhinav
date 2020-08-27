import pandas as pd
import datetime
l=pd.date_range('01-22-2020',(datetime.date.today()-datetime.timedelta(days=1)).strftime('%m-%d-%Y')).strftime('%m-%d-%Y').tolist()
df=pd.DataFrame()
for i in l:
    try:
        temp_df=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'+i+'.csv')
    except:
        continue
    len_col=len(temp_df.columns)
    cols=['FIPS','Admin2','Province_State','Country_Region','Last_Update','Lat','Long_','Confirmed','Deaths','Recovered','Active']
    try:
        if len_col==6:
            temp_df=temp_df.rename(columns={'Province/State':'Province_State','Country/Region':'Country_Region'})
            temp_df[['Confirmed','Deaths','Recovered']]=temp_df[['Confirmed','Deaths','Recovered']].fillna(0)
            temp_df['Last_Update']=i
            temp_df['Active']=list(map(int,temp_df['Confirmed']-temp_df['Deaths']-temp_df['Recovered']))
            temp_df['Lat']=''
            temp_df['Long_']=''
            temp_df['FIPS']=''
            temp_df['Admin2']=''
            df=df.append(temp_df[cols],ignore_index=True)
        elif len_col==8:
            temp_df=temp_df.rename(columns={'Province/State':'Province_State','Country/Region':'Country_Region','Latitude':'Lat','Longitude':'Long_'})
            temp_df[['Confirmed','Deaths','Recovered']]=temp_df[['Confirmed','Deaths','Recovered']].fillna(0)
            temp_df['Last_Update']=i
            temp_df['Active']=list(map(int,temp_df['Confirmed']-temp_df['Deaths']-temp_df['Recovered']))
            temp_df['FIPS']=''
            temp_df['Admin2']=''
            df=df.append(temp_df[cols],ignore_index=True)
        elif len_col==12 or len_col==14:
            temp_df['Last_Update']=i
            df=df.append(temp_df[cols],ignore_index=True)
    except:
        continue
df=df.rename(columns={'Province_State':'Province/State','Country_Region':'Country','Lat':'Latitude','Long_':'Longitude','Admin2':'County'})
df=df.replace(to_replace=['Mainland China','Bahamas, The','Gambia, The','Hong Kong SAR','Iran (Islamic Republic of)','Korea, South','Viet Nam','UK','Taiwan*','Bahamas','Taipei and environs','Russian Federation','St. Martin'],value=['China','The Bahamas','Gambia','Hong Kong','Iran','South Korea','Vietnam','United Kingdom','Taiwan','The Bahamas','Taiwan','Russia','Saint Martin'])
df_new=pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv')
l=['location','population','population_density','median_age','aged_65_older','aged_70_older','gdp_per_capita','extreme_poverty','hospital_beds_per_thousand','life_expectancy']
df_new=df_new[l]
df_new.drop_duplicates(subset='location',keep='last',inplace=True)
df_new=df_new.rename(columns={'location':'Country'})
df_new=df_new.replace(to_replace='United States',value='US')
df=pd.merge(df,df_new,how='left',left_on='Country',right_on='Country')
writer=pd.ExcelWriter('WorldHistoricalData.xlsx',engine='xlsxwriter')
df.to_excel(writer,sheet_name='Sheet1',index=False)
writer.save()
