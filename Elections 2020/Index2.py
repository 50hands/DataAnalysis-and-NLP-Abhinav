from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import numpy as np
df=pd.read_excel('50 Hands/Elections 2020/ElectionStateLinks.xlsx',sheet_name='Sheet1')
df_counties=pd.DataFrame(columns=['state','stategopvotesper','statedemvotesper'])
checklist=[]
for i in df['link'].tolist()[::-1]:
    s=i.split('/')[-2]
    if '-' in s:
        s=' '.join(s.split('-'))
    print('Extracting from '+s+'......')
    l3=[]
    l4=[]
    bot=webdriver.Chrome()
    bot.get(i)
    time.sleep(1)
    try:
        l2_win=bot.find_elements_by_class_name('winner')
        temp=l2_win[0].get_attribute('class').split(' ')[-1]
        l2=bot.find_elements_by_class_name('candidate-percent-only')
        if 'gop' in temp:
            l3.append(l2[0].get_attribute('innerHTML'))
            l4.append(l2[1].get_attribute('innerHTML'))
        else:
            l4.append(l2[0].get_attribute('innerHTML'))
            l3.append(l2[1].get_attribute('innerHTML'))
        df_states=pd.DataFrame({'state':s,'stategopvotesper':l3,'statedemvotesper':l4})
        print(df_states)
        df_counties=df_counties.append(df_states)
        bot.close()
        bot.quit()
    except:
        print('Information could not be extracted from '+s)
        continue
print('The final database is:')
print(df_counties)
writer=pd.ExcelWriter('50 Hands/Elections 2020/ElectionStateResults.xlsx',engine='xlsxwriter')
df_counties.to_excel(writer,sheet_name='Sheet1',index=False)
writer.save()
for i in checklist:
    print(i)
