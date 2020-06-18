import pandas as pd
D1=pd.read_excel('50 Hands/Poo.xlsx',sheet_name='covid_cases_raw_data')
D2=pd.read_excel('50 Hands/Poo.xlsx',sheet_name='covid_cases_stats_by_province')
D3=pd.read_excel('50 Hands/Poo.xlsx',sheet_name='covid_mortality_raw_data')
df2=pd.read_excel('50 Hands/Poo.xlsx',sheet_name='countries')
df3=pd.read_excel('50 Hands/Poo.xlsx',sheet_name='provinces')
print('Done loading databases!!')
D1=pd.merge(D1,df2,how='left',left_on='country_id',right_on='country_id')
D1=pd.merge(D1,df3,how='left',left_on='province_id',right_on='province_id')
D2=pd.merge(D2,df2,how='left',left_on='country_id',right_on='country_id')
D2=pd.merge(D2,df3,how='left',left_on='province_id',right_on='province_id')
D3=pd.merge(D3,df2,how='left',left_on='country_id',right_on='country_id')
D3=pd.merge(D3,df3,how='left',left_on='province_id',right_on='province_id')
print('Done merging!!')
origcol=['death_cases','recovered_cases','today_cases','total_cases','date','country_name','province_name']
origcol2=['total_cases','death_cases','recovered_cases','country_name','province_name']
origcol3=['age','date_report','health_region','province_death_id','sex','country_name','province_name']
D1=D1[origcol]
D2=D2[origcol2]
D3=D3[origcol3]
print('Final cleaning done!!')
writer1=pd.ExcelWriter('50 Hands/CovidDataCases.xlsx',engine='xlsxwriter')
D1.to_excel(writer1,sheet_name='Sheet1')
writer1.save()
print('File 1 done!!')
writer2=pd.ExcelWriter('50 Hands/CovidDataProvinces.xlsx',engine='xlsxwriter')
D2.to_excel(writer2,sheet_name='Sheet1')
writer2.save()
print('File 2 done!!')
writer3=pd.ExcelWriter('50 Hands/CovidDataDeath.xlsx',engine='xlsxwriter')
D3.to_excel(writer3,sheet_name='Sheet1')
writer3.save()
print('File 3 done!!')
