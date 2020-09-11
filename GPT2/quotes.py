import json
import pandas as pd
df=pd.read_json('50 Hands/GPT2/quotes.json')
l=df['Quote'].tolist()
l=list(set(l))
c=0
for i in l:
    try:
        print(c)
        f=open('50 Hands/GPT2/Quotes/'+str(c)+'.txt','a')
        f.write(i)
        f.close()
        c+=1
    except:
        continue
