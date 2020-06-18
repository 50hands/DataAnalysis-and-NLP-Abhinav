from wwo_hist import retrieve_hist_data
import os
import urllib.request
import numpy as np
import pandas as pd
import datetime
df2=pd.read_excel('50 Hands/CovidDataWeatherHistoryRegion.xlsx',sheet_name='Sheet1')
'''for i in range(len(df2)):
    if i>=8855:
        if isinstance(df2.loc[i,'date_report'],datetime.datetime):
            df2.loc[i,'date_report']=df2.loc[i,'date_report'].strftime("%m-%d-%Y")
        else:
            s=df2.loc[i,'date_report'].split('-')
            df2.loc[i,'date_report']=s[1]+'-'+s[0]+'-'+s[2]'''
df=pd.read_excel('50 Hands/CovidData.xlsx',sheet_name='Sheet1')
df3=pd.merge(df,df2,how='left',left_on=['health_region','date_report'],right_on=['health_region','date_report'])
writer=pd.ExcelWriter('50 Hands/CovidDataWeatherRegion.xlsx',engine='xlsxwriter')
df3.to_excel(writer,sheet_name='Sheet1')
writer.save()
print(df3)
