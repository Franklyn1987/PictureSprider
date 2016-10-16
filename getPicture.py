from sgmllib import SGMLParser
from bs4 import BeautifulSoup
import requests
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')


#params = {'tags': '"doll"'}
#r = requests.post("http://e-shuushuu.net/search/process/", data=params)
#print r.text

soup=BeautifulSoup(open("index.html"),"html.parser")


