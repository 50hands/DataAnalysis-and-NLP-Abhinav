import pandas as pd
df=pd.read_excel('50 Hands/USA/USAStateData2.xlsx',sheet_name='Sheet1')
s1=0
n1=0
s2=0
n2=0
for i in range(len(df)):
    s=''
    if isinstance(df.loc[i,'pop_den_per_sq_mile'],str)==True:
        for j in df.loc[i,'pop_den_per_sq_mile']:
            if j!=',':
                s=s+j
        if float(s)<190.8:
            s1=s1+float(df.loc[i,'Confirmed'])
            n1+=1
        else:
            s2=s2+float(df.loc[i,'Confirmed'])
            n2+=1
    else:
        if float(df.loc[i,'pop_den_per_sq_mile'])<190.8:
            s1=s1+float(df.loc[i,'Confirmed'])
            n1+=1
        else:
            s2=s2+float(df.loc[i,'Confirmed'])
            n2+=1
print('Above average:',round(s2/n2))
print('Below average:',round(s1/n1))
