from sgmllib import SGMLParser
from bs4 import BeautifulSoup
import urllib
import os
import requests
import re
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')


#params = {'tags': '"doll"'}
#r = requests.post("http://e-shuushuu.net/search/process/", data=params)
#print r.text

soup=BeautifulSoup(open("index.html"),"html.parser")
imageTages=soup.find_all(class_='thumb_image')


nameList=[]
hrefList=[]


for tag in imageTages:
    hrefList.append("http://e-shuushuu.net"+tag['href'].__str__())
    nameList.append("."+tag['href'].__str__())


if not os.path.exists('./images/'):
    os.mkdir('./images/')

for index in range(0,len(nameList)):
    conn = urllib.urlopen(hrefList[index])
    f = open(nameList[index],'wb')
    f.write(conn.read())
    f.close()
    print('Pic Saved!')



