import re
import urllib2
import os
import urllib
import datetime

enable_proxy = 0  
proxy_handler = urllib2.ProxyHandler({"http" : 'proxy-bj1.petrochina:8080'})  
null_proxy_handler = urllib2.ProxyHandler({})  
if enable_proxy:  
	opener = urllib2.build_opener(proxy_handler)  
else:  
	opener = urllib2.build_opener(null_proxy_handler)  
urllib2.install_opener(opener)  

url="http://www.npr.org/programs/ask-me-another/?showDate=2014-10-29"
storeDir=datetime.date.today().strftime("%Y%m%d")
if not os.path.exists(storeDir):
    os.mkdir(storeDir)
    print storeDir+"has created"
else:
    storeDir+"exists"


try:
	print "start:"
	req=urllib2.Request(url)
	response=urllib2.urlopen(req)
	if response.code==200:
		html=response.read()
		fileHtml=open('npr.txt','w')
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
				fileHtml.write(downloadMp3Str+"\n")
		
		##print re.findall('download.*Download',html)
		fileHtml.close()
	print "Job is OK:\n"
except urllib2.HTTPError,e:
	print "server error"
	print e.code
except urllib2.URLError,e:
	print "URLError:"
	print e.reason
