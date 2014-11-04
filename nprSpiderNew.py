import datetime
from bs4 import BeautifulSoup
import urllib2
import re
import ConfigParser
import os

def writeConfig(websites):
    cf=ConfigParser.ConfigParser()
    configFilePath="config.ini"
    #cf.read(configFilePath)
    if os.path.isfile(configFilePath):
            os.remove(configFilePath)
    cf.add_section('webDir')  
    cf.set('webDir','websites',websites)
    ##jjcf.set('proxy','port','80')
    cf.write(open(configFilePath,"w")) 
enable_proxy = 1  
proxy_handler = urllib2.ProxyHandler({"http" : 'proxy-bj1.petrochina:8080'})  
null_proxy_handler = urllib2.ProxyHandler({})  
if enable_proxy:  
	opener = urllib2.build_opener(proxy_handler)  
else:  
	opener = urllib2.build_opener(null_proxy_handler)  
urllib2.install_opener(opener)  
url="http://www.npr.org"
html_page = urllib2.urlopen(url)
##file_savelink=open("fileSave.txt","w")
print "starting:"
soup = BeautifulSoup(html_page)
globalheader=soup.find("header",{'id':"globalheader"})
webs=[]
for link in globalheader.findAll('a'):
    sLink=str(link.get('href'))
    if (sLink.find('section')==True):
        webs.append(url+sLink)
        print sLink
writeConfig('|'.join(webs))

storeDir=datetime.date.today().strftime("%Y%m%d")

if not os.path.exists(storeDir):
    os.mkdir(storeDir)
    print storeDir+"has created"
else:
    storeDir+"exists"


for urlLink in webs:
    try:
        print "start:"+urlLink
        req=urllib2.Request(urlLink)
        response=urllib2.urlopen(req)
        if response.code==200:
            html=response.read()
            for str1 in re.findall('download.*mp3\>?',html):
                    downloadMp3Str=str1.replace("download\"><a href=\"","")
                    print downloadMp3Str
                    mp3Name=os.path.basename(downloadMp3Str)
                    mp3Path=os.path.join(storeDir,mp3Name)
                    if os.path.exists(mp3Path):
                            pass
                    else:
                            with open(mp3Path,'wb') as fMp3:
                                fMp3.write(urllib2.urlopen(downloadMp3Str).read())
                                fMp3.close()
                                print mp3Path+" has saved."
            
            ##print re.findall('download.*Download',html)
        print "Job is OK:\n"
    except urllib2.HTTPError,e:
        print "server error"
        print e.code
    except urllib2.URLError,e:
        print "URLError:"
        print e.reason
