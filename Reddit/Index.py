import re
import string
import numpy as np
import praw
import pandas as pd
import datetime
import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords,twitter_samples
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer
from googletrans import Translator
import warnings
warnings.filterwarnings('ignore')
def RedditSub(sr):
    d={'title':[],'text':[],'totaltext':[],'date':[],'score':[]}
    for i in reddit.subreddit(sr).hot(limit=None):
        d['title'].append(i.title)
        d['text'].append(i.selftext)
        d['totaltext'].append(i.title+' '+i.selftext)
        d['date'].append(datetime.datetime.fromtimestamp(i.created))
    if 'mx' in sr or 'DACH' in sr or 'br' in sr or 'PH' in sr or 'Argentina' in sr:
        l=[]
        for i in d['totaltext']:
            translator=Translator()
            l.append(translator.translate(i).text)
        d['totaltext']=l
    return d
def sentiment_scores(sentence):
    for i in d['totaltext']:
        sid_obj=SentimentIntensityAnalyzer()
        sentiment_dict=sid_obj.polarity_scores(i)
        d['score'].append(sentiment_dict['compound'])
    return d
def process_tweet(tweet):
    stemmer=PorterStemmer()
    stopwords_english=stopwords.words('english')
    tweet=re.sub(r'\$\w*','',tweet)
    tweet=re.sub(r'^RT[\s]+', '',tweet)
    tweet=re.sub(r'https?:\/\/.*[\r\n]*','',tweet)
    tweet=re.sub(r'#', '', tweet)
    tokenizer=TweetTokenizer(preserve_case=False,strip_handles=True,reduce_len=True)
    tweet_tokens=tokenizer.tokenize(tweet)
    tweets_clean=[]
    for word in tweet_tokens:
        if (word not in stopwords_english and word not in string.punctuation):
            stem_word=stemmer.stem(word)
            tweets_clean.append(stem_word)
    return tweets_clean
def build_freqs(tweets,ys):
    yslist=np.squeeze(ys).tolist()
    freqs={}
    for y,tweet in zip(yslist,tweets):
        for word in process_tweet(tweet):
            pair=(word,y)
            if pair in freqs:
                freqs[pair]+=1
            else:
                freqs[pair]=1
    return freqs
def sigmoid(z):
    h=1/(1+np.exp(-z))
    return h
def gradientDescent(x,y,theta,alpha,num_iters):
    m=len(x)
    for i in range(0,num_iters):
        z=np.dot(x,theta)
        h=sigmoid(z)
        J=(-1/float(m))*((np.dot(y.T,np.log(h)))+(np.dot((1-y).T,np.log(1-h))))
        theta=theta-((alpha/m)*np.dot(np.transpose(x),(h-y)))
    J=float(J)
    return J,theta
def extract_features(tweet,freqs):
    word_l=process_tweet(tweet)
    x=np.zeros((1, 3))
    x[0,0]=1
    for word in word_l:
        try:
            x[0,1]+=freqs[(word,1.0)]
        except:
            continue
        try:
            x[0,2]+=freqs[(word,0.0)]
        except:
            continue
    assert(x.shape==(1, 3))
    return x
def predict_tweet(tweet,freqs,theta):
    x=extract_features(tweet,freqs)
    y_pred=sigmoid(np.dot(x,theta))
    return y_pred
def test_logistic_regression(test_x,test_y,freqs,theta):
    y_hat=[]
    for tweet in test_x:
        y_pred=predict_tweet(tweet, freqs, theta)
        if y_pred>0.5:
            y_hat.append(1)
        else:
            y_hat.append(0)
    su=0
    for i in range(len(test_y)):
        if int(test_y[i])==y_hat[i]:
            su+=1
    accuracy=su/len(test_y)
    return accuracy
def SentimentML(df):
    all_positive_tweets=twitter_samples.strings('positive_tweets.json')
    all_negative_tweets=twitter_samples.strings('negative_tweets.json')
    test_pos=all_positive_tweets[4000:]
    train_pos=all_positive_tweets[:4000]
    test_neg=all_negative_tweets[4000:]
    train_neg=all_negative_tweets[:4000]
    train_x=train_pos+train_neg
    test_x=test_pos+test_neg
    train_y=np.append(np.ones((len(train_pos),1)),np.zeros((len(train_neg),1)),axis=0)
    test_y=np.append(np.ones((len(test_pos),1)),np.zeros((len(test_neg),1)),axis=0)
    freqs=build_freqs(train_x,train_y)
    X=np.zeros((len(train_x),3))
    for i in range(len(train_x)):
        X[i,:]= extract_features(train_x[i],freqs)
    Y=train_y
    J,theta=gradientDescent(X,Y,np.zeros((3,1)),1e-9,1500)
    tmp_accuracy=test_logistic_regression(test_x,test_y,freqs,theta)
    sentiment_l=[]
    l=df['totaltext'].tolist()
    for i in l:
        y_hat=predict_tweet(i,freqs,theta)
        if y_hat>0.5:
            sentiment_l.append('Positive sentiment')
        else:
            sentiment_l.append('Negative sentiment')
    df.insert(6,'sentiment_description',sentiment_l)
    return df
if __name__=='__main__':
    df=pd.DataFrame()
    reddit=praw.Reddit(client_id='AufQL3euwJJj4g',client_secret='LptAeUr3_VeykZewe6W2hTa7d7w',password='Babie123$%^',user_agent='Test Script by /u/abhinavnope',username='abhinavnope')
    srl=['CoronavirusDACH','covidmx','coronabr','Coronavirus_PH','CoronavirusArgentina','CoronavirusIndia','CanadaCoronavirus','CoronavirusCanada','CoronavirusUS','CoronavirusUK','Coronavirusdownunder','CoronavirusJapan']
    for i in srl:
        d=RedditSub(i)
        d=sentiment_scores(d)
        if 'US' in i:
            d['country']='United States'
        elif 'DACH' in i:
            d['country']='Germany'
        elif 'Canada' in i:
            d['country']='Canada'
        elif 'India' in i:
            d['country']='India'
        elif 'downunder' in i:
            d['country']='Australia'
        elif 'UK' in i:
            d['country']='United Kingdom'
        elif 'Japan' in i:
            d['country']='Japan'
        elif 'mx' in i:
            d['country']='Mexico'
        elif 'br' in i:
            d['country']='Brazil'
        elif 'PH' in i:
            d['country']='Philippines'
        elif 'Argentina' in i:
            d['country']='Argentina'
        df=df.append(pd.DataFrame(d),ignore_index=True)
    df['score']=df['score'].map(lambda x:round(x,4))
    df=SentimentML(df)
    df=df.fillna('')
    df=df.replace(to_replace=' ',value='')
    writer=pd.ExcelWriter('TReddit.xlsx',engine='xlsxwriter')
    df.to_excel(writer,sheet_name='Sheet1',index=False)
    writer.save()
