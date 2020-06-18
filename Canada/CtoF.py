import pandas as pd
df=pd.read_excel('50 Hands/CovidDataWeatherRegion.xlsx',sheet_name='Sheet1')
l=['Montérégie','Estrie','Nunavik','Lanaudière','Outaouais']
for i in range(len(df)):
    if df.loc[i,'health_region'] not in l:
        df.loc[i,'tempC']=(df.loc[i,'tempC']*1.8)+32
writer=pd.ExcelWriter('50 Hands/CovidDataWeatherRegion2.xlsx',engine='xlsxwriter')
df.to_excel(writer,sheet_name='Sheet1')
writer.save()
