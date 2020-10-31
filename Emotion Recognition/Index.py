import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'
import tensorflow as tf
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import time
import warnings
from PIL import Image
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
warnings.filterwarnings('ignore')
def emotion_analysis(emotions):
    objects=('angry','disgust','fear','happy','sad','surprise','neutral')
    y_pos=np.arange(len(objects))
    emotion=objects[(emotions.tolist()).index(max(emotions))]
    return objects,y_pos,emotion
def uploadimage(model,faceCascade,filename):
    image=cv2.imread(filename)
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=3,minSize=(30,30))
    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
        roi_color=image[y:y+h,x:x+w]
        stri='C:/Users/ABHINAV/Desktop/MYFiles/Data Science and Machine Learning Specializations/50 Hands/Emotion Recognition/images/targetface.jpg'
        cv2.imwrite(stri,roi_color)
    img=tf.keras.preprocessing.image.load_img(stri,color_mode='grayscale',target_size=(48,48))
    x=tf.keras.preprocessing.image.img_to_array(img)
    x=np.expand_dims(x,axis=0)
    x/=255
    custom=model.predict(x)
    objects,y_pos,emotion=emotion_analysis(custom[0])
    if os.path.exists(stri):
        os.remove(stri)
    return objects,y_pos,emotion,custom[0]
def opencamera(model,faceCascade):
    emotions=('angry','disgust','fear','happy','sad','surprise','neutral')
    cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
    frame=0
    dict={'angry':[],'disgust':[],'fear':[],'happy':[],'sad':[],'surprise':[],'neutral':[]}
    while(True):
        ret,img=cap.read()
        img=cv2.resize(img,(640,360))
        img=img[0:308,:]
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in faces:
            if w>130:
                cv2.rectangle(img,(x,y),(x+w,y+h),(64,64,64),2)
                detectedface=img[int(y):int(y+h),int(x):int(x+w)]
                detectedface=cv2.cvtColor(detectedface,cv2.COLOR_BGR2GRAY)
                detectedface=cv2.resize(detectedface,(48,48))
                img_pixels=tf.keras.preprocessing.image.img_to_array(detectedface)
                img_pixels=np.expand_dims(img_pixels,axis=0)
                img_pixels/=255
                predictions=model.predict(img_pixels)
                max_index=np.argmax(predictions[0])
                overlay=img.copy()
                opacity=0.4
                cv2.rectangle(img,(x+w+10,y-25),(x+w+150,y+115),(64,64,64),cv2.FILLED)
                cv2.addWeighted(overlay,opacity,img,1-opacity,0,img)
                cv2.line(img,(int((x+x+w)/2),y+15),(x+w,y-20),(255,255,255),1)
                cv2.line(img,(x+w,y-20),(x+w+10,y-20),(255,255,255),1)
                emotion=''
                for i in range(len(predictions[0])):
                    emotion='%s %s%s'%(emotions[i],round(predictions[0][i]*100,2),'%')
                    dict[emotions[i]].append(round(predictions[0][i]*100,2))
                    color=(255,255,255)
                    cv2.putText(img,emotion,(int(x+w+15),int(y-12+i*20)),cv2.FONT_HERSHEY_SIMPLEX,0.5,color,1)
        cv2.imshow('img',img)
        frame=frame+1
        if frame>50:
            break
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    emotionlist=[]
    for i in dict.items():
        emotionlist.append(np.mean(dict[i[0]]))
    return emotionlist,emotions
def ImageBasedDetection():
    faceCascade=cv2.CascadeClassifier('C:/Users/ABHINAV/Desktop/MYFiles/Data Science and Machine Learning Specializations/50 Hands/Emotion Recognition/haarcascade_frontalface_default.xml')
    model=tf.keras.models.load_model('C:/Users/ABHINAV/Desktop/MYFiles/Data Science and Machine Learning Specializations/50 Hands/Emotion Recognition/model',custom_objects=None,compile=True,options=None)
    print('You have two options.')
    print('Press 1: Upload an image.')
    print('Press 2: Open camera.')
    choice2=int(input())
    if choice2==1:
        Tk().withdraw()
        filename=askopenfilename()
        objects,y_pos,emotion,emotions=uploadimage(model,faceCascade,filename)
        plt.figure(figsize=(14,6))
        plt.subplot(121)
        plt.imshow(cv2.cvtColor(cv2.imread(filename),cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.subplot(122)
        plt.bar(y_pos,emotions,align='center',alpha=0.5)
        plt.xticks(y_pos,objects)
        plt.ylabel('Percentage')
        tit='The person is '+emotion+'!!!'
        plt.title(tit)
        stri='C:/Users/ABHINAV/Desktop/MYFiles/Data Science and Machine Learning Specializations/50 Hands/Emotion Recognition/emotions.png'
        plt.savefig(stri)
        image=Image.open(stri)
        image.show()
        time.sleep(25)
        if os.path.exists(stri):
            os.remove(stri)
        return emotions,objects
    elif choice2==2:
        emotionlist,emotions=opencamera(model,faceCascade)
        emotionlist2=[]
        for i in emotionlist:
            emotionlist2.append(round(float(i*100/sum(emotionlist)),4))
        plt.figure(figsize=(6,6))
        plt.bar(np.arange(len(emotions)),emotionlist2,align='center',alpha=0.5)
        plt.xticks(np.arange(len(emotions)),emotions)
        plt.ylabel('Percentage')
        tit='The person is '+list(emotions)[np.argmax(emotionlist)]+'!!!'
        plt.title(tit)
        stri='C:/Users/ABHINAV/Desktop/MYFiles/Data Science and Machine Learning Specializations/50 Hands/Emotion Recognition/emotions.png'
        plt.savefig(stri)
        image=Image.open(stri)
        image.show()
        time.sleep(25)
        if os.path.exists(stri):
            os.remove(stri)
        return emotionlist2,emotions
def TextBasedEmotion():
    l=[]
    print('When I got up in the morning, I felt\nA. Moody & Irritable\nB. Uneasy\nC. Enthusiastic\nD. Affectionate\nE. Downhearted\nF. Joyous')
    inp=input().strip()
    d={'a':'When I got up in the morning, I felt Moody and Irritable','b':'When I got up in the morning, I felt Uneasy','c':'When I got up in the morning, I felt Enthusiastic','d':'When I got up in the morning, I felt Affectionate','e':'When I got up in the morning, I felt Downhearted','f':'When I got up in the morning, I felt Joyous'}
    l.append(d[inp.lower()].lower())
    print('How well do you sleep usually?\nA. I have a healthy sleeping pattern.\nB. I sleep fine most nights.\nC. I sleep too much, cannot seem to get myself out of bed.\nD. I have a hard time falling or staying asleep.\nE. I have frequent nightmares.\nF. I frequently wake up feeling angry or dissatisfied.')
    inp=input().lower()
    d={'a':'I have a healthy sleeping pattern.','b':'I sleep fine most nights.','c':'I sleep too much, cannot seem to get myself out of bed.','d':'I have a hard time falling or staying asleep.','e':'I have frequent nightmares.','f':'I frequently wake up feeling angry or dissatisfied.'}
    l.append(d[inp.lower()].lower())
    print('How easy is it to talk about your feelings?\nA. Talking about my feelings brings me joy.\nB. I do not have anyone to talk to about my feelings.\nC. Some feelings are hard to talk about, but I do it because I know it is healthy to talk things out.\nD. I do not trust anyone so I have a hard time opening up to others.\nE. I find it impossible to talk about my feelings.\nF. The idea of talking about feelings makes me angry.')
    inp=input().lower()
    d={'a':'Talking about my feelings brings me joy.','b':'I do not have anyone to talk to about my feelings.','c':'Some feelings are hard to talk about, but I do it because I know it is healthy to talk things out.','d':'I do not trust anyone so I have a hard time opening up to others.','e':'I find it impossible to talk about my feelings.','f':'The idea of talking about feelings makes me angry.'}
    l.append(d[inp.lower()].lower())
    print('How would you describe your heartbeat right now?\nA. Super fast.\nB. Happily.\nC. Slowly, barely keeping me alive.')
    inp=input().lower()
    d={'a':'My heart is beating Super fast.','b':'My heart is beating Happily.','c':'My heart is beating Slowly, barely keeping me alive.'}
    l.append(d[inp.lower()].lower())
    print('Did something negative happen recently?\nA. No, everything has been great!!\nB. I woke up tensed and anxious.\nC. Yes and it was not fair.\nD. Yes, something bad happened recently.\nE. No, but I have the feeling something bad will happen soon!')
    inp=input().lower()
    d={'a':'No, everything has been great!!','b':'I woke up tensed and anxious.','c':'Yes and it was not fair.','d':'Yes, something bad happened recently.','e':'No, but I have the feeling something bad will happen soon!'}
    l.append(d[inp.lower()].lower())
    print('What would you do during a traffic jam?\nA. Honk my horn and give people the finger.\nB. Play my favourite song on repeat.\nC. Just sit there and endure.\nD. Check my phone for new messages.\nE. Keep checking my watch and calculating how many minutes I have left to arrive on time.\nF. Smile and wink at other drivers.')
    inp=input().lower()
    d={'a':'Honk my horn and give people the finger.','b':'Play my favourite song on repeat.','c':'Just sit there and endure.','d':'Check my phone for new messages.','e':'Keep checking my watch and calculating how many minutes I have left to arrive on time.','f':'Smile and wink at other drivers.'}
    l.append(d[inp.lower()].lower())
    print('Have you recently done any activities that make you happy?\nA. Yes, I frequently do things that make me happy.\nB. No, I have not had the time.')
    inp=input().lower()
    d={'a':'Yes, I frequently do things that make me happy.','b':'No, I have not had the time.'}
    l.append(d[inp.lower()].lower())
    print('How do you feel about yourself right now?\nA. I am proud of myself.\nB. I am better than everyone.\nC. I am the worst.\nD. I am scared about the future.')
    inp=input().lower()
    d={'a':'I am proud of myself.','b':'I am better than everyone.','c':'I am the worst.','d':'I am scared about the future.'}
    l.append(d[inp.lower()].lower())
    print('Assume you just finished an important task, what would you do on the following weekend?\nA. Go to a party and have fun.\nB. Stay at home and read.\nC. Hangout with my friends.\nD. Stay at home and think about what the future holds.\nE. Do nothing.')
    inp=input().lower()
    d={'a':'Go to a party and have fun.','b':'Stay at home and read.','c':'Hangout with my friends.','d':'Stay at home and think about what the future holds.','e':'Do nothing.'}
    l.append(d[inp.lower()].lower())
    emotionlist,emotions=textmodel(l)
    return emotionlist,emotions
def textmodel(message):
    emotions=('happy','fear','angry','sad','neutral')
    mat=textemotionscore(message)
    l=np.array([0,0,0,0,0],dtype='float')
    for i in mat:
        l=l+np.array([round(j,2) for j in i])
    emotionlist=[round(i*100/9,4) for i in l.tolist()]
    plt.figure(figsize=(6,6))
    plt.bar(np.arange(5),emotionlist,align='center',alpha=0.5)
    plt.xticks(np.arange(5),emotions)
    plt.ylabel('Percentage')
    tit='The person is '+list(emotions)[np.argmax(emotionlist)]+'!!!'
    plt.title(tit)
    stri='C:/Users/ABHINAV/Desktop/MYFiles/Data Science and Machine Learning Specializations/50 Hands/Emotion Recognition/emotions.png'
    plt.savefig(stri)
    image=Image.open(stri)
    image.show()
    time.sleep(25)
    if os.path.exists(stri):
        os.remove(stri)
    return emotionlist,emotions
def textemotionscore(message):
    num_classes=5
    embed_num_dims=300
    max_seq_len=500
    tokenizer=Tokenizer()
    tokenizer.fit_on_texts(pd.read_excel('C:/Users/ABHINAV/Desktop/MYFiles/Data Science and Machine Learning Specializations/50 Hands/Emotion Recognition/TextModelFiles/Texts.xlsx',sheet_name='Sheet1')['Text'].tolist())
    embedd_matrix=np.load('C:/Users/ABHINAV/Desktop/MYFiles/Data Science and Machine Learning Specializations/50 Hands/Emotion Recognition/TextModelFiles/Embeddmatrix.npy')
    textmodel=tf.keras.models.load_model('C:/Users/ABHINAV/Desktop/MYFiles/Data Science and Machine Learning Specializations/50 Hands/Emotion Recognition/textmodel',custom_objects=None,compile=True,options=None)
    seq=tokenizer.texts_to_sequences(message)
    padded=pad_sequences(seq,maxlen=max_seq_len)
    pred=textmodel.predict(padded)
    pred=pred.tolist()
    return pred
if __name__=='__main__':
    print('You have three options.')
    print('Press 1: Text based emotion detection.')
    print('Press 2: Image based emotion detection.')
    print('Press 3: For text and image based emotion detection.')
    choice=int(input())
    df=pd.read_excel('C:/Users/ABHINAV/Desktop/MYFiles/Data Science and Machine Learning Specializations/50 Hands/Emotion Recognition/EmotionSongs.xlsx',sheet_name='Sheet1')
    if choice==1:
        emovalues,emolist=TextBasedEmotion()
        df=df[df['emotion']==list(emolist)[np.argmax(emovalues)]].reset_index(drop=True)
        print('\nThe suggested songs are:\n')
        for i in range(30):
            print('Track:',df.loc[i]['track'])
            print('Album:',df.loc[i]['album'])
            print('Artists:',df.loc[i]['artists'])
            print('Song URL:',df.loc[i]['url']+'\n')
    elif choice==2:
        emovalues,emolist=ImageBasedDetection()
        df=df[df['emotion']==list(emolist)[np.argmax(emovalues)]].reset_index(drop=True)
        print('\nThe suggested songs are:\n')
        for i in range(30):
            print('Track:',df.loc[i]['track'])
            print('Album:',df.loc[i]['album'])
            print('Artists:',df.loc[i]['artists'])
            print('Song URL:',df.loc[i]['url']+'\n')
    elif choice==3:
        emovalues,emolist=ImageBasedDetection()
        emovalues2=[round(float(i),4) for i in emovalues]
        emovalues[0]/=2
        emovalues[2]/=2
        emovalues[3]/=2
        emovalues[4]/=2
        emovalues[6]/=2
