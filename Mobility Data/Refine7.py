import pandas as pd
'''df=pd.read_excel('50 Hands/USA/Poo.xlsx',sheet_name='US_county_population')
df=df[['state_name','county_name','total_population']]
df=df.rename(columns={'state_name':'sub_region_1','county_name':'sub_region_2'})
df.insert(3,'country_region','United States')
df2=pd.read_excel('50 Hands/USA/Poo.xlsx',sheet_name='US_state_population')
df2=df2[['state_name','total']]
df2=df2.rename(columns={'state_name':'sub_region_1','total':'total_population'})
df2.insert(2,'country_region','United States')
df2.insert(3,'sub_region_2','(Base Level)')
df=df.append(df2,ignore_index=True)
writer=pd.ExcelWriter('50 Hands/Mobility Data/CountyPopulation.xlsx',engine='xlsxwriter')
df.to_excel(writer,sheet_name='Sheet1',index=False)
writer.save()'''
df=pd.read_excel('50 Hands/Mobility Data/GoogleMobilityData.xlsx',sheet_name='Sheet1')
df2=pd.read_excel('50 Hands/Mobility Data/CountyPopulation.xlsx',sheet_name='Sheet1')
df=pd.merge(df,df2,how='left',left_on=['country_region','sub_region_1','sub_region_2'],right_on=['country_region','sub_region_1','sub_region_2'])
writer=pd.ExcelWriter('50 Hands/Mobility Data/GoogleMobilityData2.xlsx',engine='xlsxwriter')
df.to_excel(writer,sheet_name='Sheet1',index=False)
writer.save()
