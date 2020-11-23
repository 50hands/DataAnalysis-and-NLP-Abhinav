import pandas as pd
from flask import Flask
from flask_restful import Resource,Api
app=Flask(__name__)
api=Api(app)
class Emotion(Resource):
    def get(self,emotion):
        df=pd.read_excel('C:/Users/ABHINAV/Desktop/MYFiles/Data Science and Machine Learning Specializations/50 Hands/Emotion Recognition/EmotionSongs.xlsx',sheet_name='Sheet1')
        df=df[df['emotion']==emotion].reset_index(drop=True)
        d={}
        for i in range(30):
            d_temp={'artists':df['artists'].tolist()[i],'album':df['album'].tolist()[i],'url':df['url'].tolist()[i]}
            d[df['track'].tolist()[i]]=d_temp
        return d
api.add_resource(Emotion,'/emotion/<string:emotion>')
if __name__=='__main__':
    app.run(debug=True)
