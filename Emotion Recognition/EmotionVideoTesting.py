import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'
import tensorflow as tf
import cv2
import numpy as np
import warnings
warnings.filterwarnings('ignore')
model=tf.keras.models.load_model('C:\\Users\\ABHINAV\\Desktop\\MYFiles\\Data Science and Machine Learning Specializations\\Softwares\\Emotion Recognition\\model',custom_objects=None,compile=True,options=None)
emotions=('angry','disgust','fear','happy','sad','surprise','neutral')
facecascade=cv2.CascadeClassifier('C:\\Users\\ABHINAV\\Desktop\\MYFiles\\Data Science and Machine Learning Specializations\\Softwares\\Emotion Recognition\\haarcascade_frontalface_default.xml')
cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
frame=0
dict={'angry':0,'disgust':0,'fear':0,'happy':0,'sad':0,'surprise':0,'neutral':0}
while(True):
    ret,img=cap.read()
    img=cv2.resize(img,(640,360))
    img=img[0:308,:]
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=facecascade.detectMultiScale(gray,1.3,5)
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
                dict[emotions[i]]+=round(predictions[0][i]*100,2)
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
print('Facial Emotion Analysis:',end='\n\n')
for i in dict.items():
    print(i[0]+':',str(round(i[1]*100/sum(list(dict.values())),2))+'%')
dict=sorted(dict.items(),key=lambda x:x[1],reverse=True)
print('\nThe prominent emotions shown are:',dict[0][0],'and',dict[1][0]+'.')
