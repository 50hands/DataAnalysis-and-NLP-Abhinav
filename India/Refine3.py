import pandas as pd
df=pd.read_excel('50 Hands/India/Poo.xlsx',sheet_name='Ind_district_lvl_upd')
df2=pd.read_excel('50 Hands/India/Poo.xlsx',sheet_name='Sheet1')
df4=pd.read_excel('50 Hands/India/Poo.xlsx',sheet_name='Ind_district_geo_loc')
df3=pd.merge(df,df2,how='left',left_on='state_id',right_on='state_id')
df5=pd.merge(df3,df4,how='left',left_on='district_name',right_on='district_name')
df5=df5.dropna()
writer=pd.ExcelWriter('50 Hands/India/CovidDataDistrictCases.xlsx',engine='xlsxwriter')
df5.to_excel(writer,sheet_name='Sheet1')
writer.save()
