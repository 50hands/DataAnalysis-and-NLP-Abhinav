import pandas as pd
df=pd.read_excel('50 Hands/India/Poo.xlsx',sheet_name='Ind_state_lvl_last_upd')
df2=pd.read_excel('50 Hands/India/Poo.xlsx',sheet_name='Sheet1')
DF=pd.merge(df,df2,how='left',left_on='state_id',right_on='statecode')
writer=pd.ExcelWriter('50 Hands/India/CovidDataStateCases.xlsx',engine='xlsxwriter')
DF.to_excel(writer,sheet_name='Sheet1')
writer.save()
