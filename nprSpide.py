import urllib2
url="www.npr.org"
try:
	response==urllib2.urlopen(url)
	if response.code=200:
		html=response.read()
except urllib2.URLError,e:
	print e.reason()
