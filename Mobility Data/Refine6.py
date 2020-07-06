import pandas as pd
df=pd.read_excel('50 Hands/Mobility Data/CountyData.xlsx',sheet_name='Sheet1')
'''df2=pd.read_excel('50 Hands/Mobility Data/HistoricalData.xlsx',sheet_name='USA_Geolocation_Data')
df.insert(6,'country_region','United States')
df=pd.merge(df2,df,how='left',left_on='state',right_on='state')
writer=pd.ExcelWriter('50 Hands/Mobility Data/CountyData.xlsx',engine='xlsxwriter')
df.to_excel(writer,sheet_name='Sheet1',index=False)
writer.save()'''
