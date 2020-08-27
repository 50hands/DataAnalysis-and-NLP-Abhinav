import praw
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd
import re
import numpy as np
import time
import datetime
def RedditSub(sr):
    l=[]
    d_tmod={'title':[],'text':[],'total_text':[]}
    if 'Canada' in sr:
        d_tmod['country']='Canada'
    elif 'India' in sr:
        d_tmod['country']='India'
    else:
        d_tmod['country']='United States'
    for i in reddit.subreddit(sr).hot(limit=None):
        if i.created>int(time.mktime(time.strptime(str(datetime.datetime.now()-datetime.timedelta(days=115)).split('.')[0],'%Y-%m-%d %H:%M:%S'))):
            f=nltk.word_tokenize(i.title+' '+i.selftext)
            l.extend([i.lower() for i in f])
            try:
                if len(i.selftext)>2:
                    d_tmod['title'].append(i.title)
                    d_tmod['text'].append(i.selftext)
                    d_tmod['total_text'].append(i.title+' '+i.selftext)
            except:
                continue
    df_temp=pd.DataFrame(d_tmod)
    l=[st.lemmatize(i,pos='v') for i in l]
    l=['cases' if i=='case' else i for i in l]
    l=['testing' if i=='test' else i for i in l]
    stop_pos=['IN','CD','MD']
    cl=[i for i in list(set(l)) if (i!='covid-19' and i!='covid' and i not in country_list and i.isalpha()==True and i!='coronavirus' and i not in stops and 25>len(i)>3 and '|' not in i and '\'' not in i and nltk.pos_tag([i])[0][1] not in stop_pos and 'http' not in i)]
    d={}
    for i in cl:
        d[i]=l.count(i)
    d=sorted(d.items(),key=lambda x:x[1],reverse=True)
    return d,df_temp
def BigramCreation(df):
    df['processedtext']=df['total_text'].map(lambda x:re.sub('[,\.!?]','',x))
    df['processedtext']=df['processedtext'].map(lambda x:x.lower())
    stop_pos=['IN','CD','MD']
    df_new=pd.DataFrame()
    for c in ['Canada','India','United States']:
        l_bigrams=[]
        df2=df[df['country']==c]
        for i in df2['processedtext']:
            try:
                l=nltk.word_tokenize(i)
                l=[st.lemmatize(j,pos='v') for j in l]
                l=['cases' if j=='case' else j for j in l]
                l=['testing' if j=='test' else j for j in l]
                l=['deceased' if j=='decease' else j for j in l]
                l=['confirmed' if j=='confirm' else j for j in l]
                l=['hospitalized' if j=='hospitalize' else j for j in l]
                l=[j for j in l if (j.isalpha()==True and j not in stops and 25>len(j)>3 and '|' not in j and '\'' not in j and nltk.pos_tag([j])[0][1] not in stop_pos and 'http' not in j)]
                l_bi=list(nltk.bigrams(l))
                l_bigrams.extend(l_bi)
            except:
                continue
        l_bigrams_uni=list(set(l_bigrams))
        d={}
        for i in l_bigrams_uni:
            d[i]=l_bigrams.count(i)
        l_del=[]
        for i in d:
            if (i[1],i[0]) in d and (i[0],i[1]) not in l_del:
                d[i]+=d[(i[1],i[0])]
                l_del.append((i[1],i[0]))
        for i in l_del:
            del d[i]
        d=sorted(d.items(),key=lambda x:x[1],reverse=True)
        l1=[]
        l2=[]
        for i in d:
            l1.append(i[0])
            l2.append(i[1])
        df_new=df_new.append(pd.DataFrame({'bis':l1,'frequency':l2,'country':c}),ignore_index=True)
    df_new['bis']=df_new['bis'].map(lambda x:str(x).replace('\'','').replace('(','').replace(')','').replace(',','').upper())
    df_new=df_new.replace('MASK WEAR','WEAR MASK')
    return df_new
if __name__=='__main__':
    reddit=praw.Reddit(client_id='AufQL3euwJJj4g',client_secret='LptAeUr3_VeykZewe6W2hTa7d7w',password='Babie123$%^',user_agent='Test Script by /u/abhinavnope',username='abhinavnope')
    st=WordNetLemmatizer()
    stops=list(set(stopwords.words('english')))
    stops.extend(['even','also'])
    country_list=['india','canada','usa','united states']
    df=pd.DataFrame()
    df_tmod=pd.DataFrame()
    srl=['CoronavirusUS','CanadaCoronavirus','CoronavirusIndia']
    for i in srl:
        d=RedditSub(i)
        df_tmod=df_tmod.append(d[1])
        if 'US' in i:
            c='United States'
        elif 'Canada' in i:
            c='Canada'
        else:
            c='India'
        temp_dict={'word':[],'frequency':[],'country':c}
        for i in d[0]:
            try:
                if i[1]>3:
                    temp_dict['word'].append(i[0].upper())
                    temp_dict['frequency'].append(i[1])
            except:
                continue
        df=df.append(pd.DataFrame(temp_dict),ignore_index=True)
    writer=pd.ExcelWriter('Words.xlsx',engine='xlsxwriter')
    df.to_excel(writer,sheet_name='Sheet1',index=False)
    writer.save()
    df_new=BigramCreation(df_tmod)
    writer=pd.ExcelWriter('TwoWords.xlsx',engine='xlsxwriter')
    df_new.to_excel(writer,sheet_name='Sheet1',index=False)
    writer.save()
