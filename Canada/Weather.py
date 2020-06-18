import pandas as pd
import numpy as np
import statsmodels.api as sm
'''df=pd.read_excel('50 Hands/CovidData.xlsx',sheet_name='Sheet1')
df2=pd.read_csv('50 Hands/CovidDataWeatherHistory.csv')
for i in range(len(df2)):
    if '/' in df2.loc[i,'date_report']:
        s=df2.loc[i,'date_report'].split('/')
        df2.loc[i,'date_report']=s[1]+'-'+s[0]+'-'+s[2]
    elif '-' in df2.loc[i,'date_report']:
        s=df2.loc[i,'date_report'].split('-')
        df2.loc[i,'date_report']=s[1]+'-'+s[0]+'-'+s[2]
df3=pd.merge(df,df2,how='left',left_on=['province_name','date_report'],right_on=['province_name','date_report'])
print(df3)'''
'''writer=pd.ExcelWriter('50 Hands/CovidDataWeather.xlsx',engine='xlsxwriter')
df3.to_excel(writer,sheet_name='Sheet1')
writer.save()'''
n1=34077223
p1=0.00230502
n2=2903911
p2=0.00024656
pop1=np.random.binomial(1,p1,n1)
pop2=np.random.binomial(1,p2,n2)
print(sm.stats.ttest_ind(pop1,pop2))
