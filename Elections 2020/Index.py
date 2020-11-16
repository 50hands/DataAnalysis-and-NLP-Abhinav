from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import numpy as np
df=pd.read_excel('ElectionStateLinks.xlsx',sheet_name='Sheet1')
df_counties=pd.DataFrame(columns=['state','county','gopvotes','demvotes'])
checklist=[]
for i in df['link'].tolist()[::-1]:
    s=i.split('/')[-2]
    if '-' in s:
        s=' '.join(s.split('-'))
    print('Extracting from '+s+'......')
    l3=[]
    l4=[]
    l5=[]
    l6=[]
    bot=webdriver.Chrome()
    bot.get(i)
    time.sleep(10)
    try:
        bot.find_element_by_xpath("//button[@class='jsx-3713440361']").click()
    except:
        pass
    time.sleep(5)
    try:
        l2=bot.find_elements_by_class_name('jsx-3648768983')
        temp=0
        for j in l2:
            lc=j.get_attribute('innerHTML')
            if 'div' not in lc:
                if temp%2==0:
                    l5.append(float(str(lc)[:len(lc)-1]))
                else:
                    l6.append(float(str(lc)[:len(lc)-1]))
                temp+=1
        l=[i.get_attribute('innerHTML') for i in bot.find_elements_by_class_name('county-name')]
        l2=bot.find_elements_by_class_name('jsx-3469064484')
        print('Data extracted from '+s+'......')
        for j in l2:
            lc=j.get_attribute('class').split(' ')
            if 'dem' in lc:
                l4.append(j.get_attribute('innerHTML').replace(',',''))
            elif 'gop' in lc:
                l3.append(j.get_attribute('innerHTML').replace(',',''))
        l3=list(map(int,l3))
        l4=list(map(int,l4))
        if sum(l3)>sum(l4):
            gopvotesper=l5
            demvotesper=l6
        else:
            gopvotesper=l6
            demvotesper=l5
        bot.close()
        bot.quit()
        df_states=pd.DataFrame({'state':s,'county':l,'gopvotes':l3,'gopvotesper':gopvotesper,'demvotes':l4,'demvotesper':demvotesper})
        print(df_states)
        df_counties=df_counties.append(df_states)
        checklist.append([i,len(df_states)])
    except:
        print('Information could not be extracted from '+s)
        continue
print('The final database is:')
print(df_counties)
writer=pd.ExcelWriter('ElectionResults.xlsx',engine='xlsxwriter')
df_counties.to_excel(writer,sheet_name='Sheet1',index=False)
writer.save()
for i in checklist:
    print(i)
