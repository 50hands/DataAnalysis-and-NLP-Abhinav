import statsmodels.api as sm
import pandas as pd
import numpy as np
df=pd.read_excel('50 Hands/CovidDataProvinces.xlsx',sheet_name='Sheet1')
n1=df[df['province_name']=='Ontario']['total_cases'].tolist()[0]
n2=df[df['province_name']=='Quebec']['total_cases'].tolist()[0]
p1=df[df['province_name']=='Ontario']['recovered_cases'].tolist()[0]/n1
p2=df[df['province_name']=='Quebec']['recovered_cases'].tolist()[0]/n2
print('For recovery rates between Ontario and Quebec:')
pop1=np.random.binomial(1,p1,n1)
pop2=np.random.binomial(1,p2,n2)
print(sm.stats.ttest_ind(pop1,pop2))
print()
df2=pd.read_excel('50 Hands/CovidData.xlsx',sheet_name='Sheet1')
df3=pd.read_excel('50 Hands/CovidDataDeath.xlsx',sheet_name='Sheet1')
n1=len(df2[df2['gender']=='Male'])
n2=len(df2[df2['gender']=='Female'])
p1=len(df3[df3['sex']=='Male'])/n1
p2=len(df3[df3['sex']=='Female'])/n2
print('For death rates between Males and Females:')
pop1=np.random.binomial(1,p1,n1)
pop2=np.random.binomial(1,p2,n2)
print(sm.stats.ttest_ind(pop1,pop2))
