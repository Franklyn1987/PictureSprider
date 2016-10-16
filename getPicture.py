from sgmllib import SGMLParser
from bs4 import BeautifulSoup
import urllib
import os
import requests

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def getPicInfoFromPage(pageFile):
    soup=BeautifulSoup(open(pageFile),"html.parser")
    picInfos=[]
    imageTages=soup.find_all(class_='thumb_image')

    for tag in imageTages:
        href="http://e-shuushuu.net"+tag['href'].__str__()
        name="."+tag['href'].__str__()
        pic=[]
        pic.append(name)
        pic.append(href)
        picInfos.append(pic)

    index=0
    for dl in soup.find_all('dl'):
        for dt in dl.find_all('dt'):
            if dt.string=='Dimensions:':
                dim=dt.next_element.next_element.next_element.string
                split1=dim.find('x')
                split2=dim.find(' ')
                picX=dim[0:split1]
                picY=dim[split1+1:split2]
                picInfos[index].append(int(picX))
                picInfos[index].append(int(picY))
                index=index+1

    return picInfos

def writePage(url,count):
    if not os.path.exists('./pages/'):
        os.mkdir('./pages/')
    page=requests.get(url)
    f=open('./pages/'+str(count)+'.html','wb')
    f.write(page.text)
    f.close()
    print (str(count)+'page saved!')


def writePic(picInfo):
    if not os.path.exists('./images/'):
        os.mkdir('./images/')
    conn = urllib.urlopen(picInfo[1])
    f = open(picInfo[0],'wb')
    f.write(conn.read())
    f.close()
    print('Pic Saved!')


def nextPageUrl(page):
    soup=BeautifulSoup(open(page),"html.parser")
    next=soup.find_all(class_='next')
    return "http://e-shuushuu.net/search/results/"+next[0].find('a')['href'].__str__()


"""-----------------------------------------------------------------------------"""
params = {'source': '"Steins;Gate"'}
#r = requests.post("http://e-shuushuu.net/search/process/", data=params)
#print r.text

maxCount=20
minX=1366
minY=768
bk=True

indexPage = requests.post("http://e-shuushuu.net/search/process/", data=params)

picCount=0
if not os.path.exists('./pages/'):
    os.mkdir('./pages/')
f=open('./pages/0.html','wb')
f.write(indexPage.text)
f.close()

picInfos=getPicInfoFromPage("./pages/0.html")



for info in picInfos:
    if info[2]>minX and info[3]>minY:
        if not bk or info[2]>info[3]:
            writePic(info)
            picCount=picCount+1
            if picCount==maxCount:
                break


pageCount=0
while picCount<maxCount:
    nextUrl=nextPageUrl('./pages/' + str(pageCount)+'.html')
    pageCount=pageCount+1
    writePage(nextUrl,pageCount)
    picInfos=getPicInfoFromPage('./pages/'+str(pageCount)+'.html')
    for info in picInfos:
        if info[2]>minX and info[3]>minY:
            writePic(info)
            picCount=picCount+1
            if picCount==maxCount:
                break

