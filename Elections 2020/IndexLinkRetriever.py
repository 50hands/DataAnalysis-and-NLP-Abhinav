from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
bot=webdriver.Chrome()
bot.get('https://www.politico.com/2020-election/results/president/')
time.sleep(10)
l=[i.get_attribute('href') for i in bot.find_elements_by_class_name('jsx-2085888330') if i.get_attribute('href')!=None]
time.sleep(4)
bot.close()
bot.quit()
x=['president','senate','house','governor','tv-network-calls','ballot-measures','poll-closing-times']
s='https://www.politico.com/2020-election/results/'
statelinks=[]
for i in l:
    if i==s:
        continue
    temp=0
    for j in x:
        if j in i:
            temp=1
            break
    if temp!=1:
        statelinks.append(i)
statelinks=sorted(list(set(statelinks)))
print(len(statelinks))
df=pd.DataFrame({'link':statelinks})
writer=pd.ExcelWriter('50 Hands/Elections 2020/ElectionStateLinks.xlsx',engine='xlsxwriter')
df.to_excel(writer,sheet_name='Sheet1',index=False)
writer.save()
