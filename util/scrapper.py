from bs4 import BeautifulSoup
import urllib2

def scrap(url):
        html = urllib2.urlopen(url).read()
        scrapper = BeautifulSoup(html,"html.parser")
        return scrapper

def parseDate(date):
	if(date>=10):
		return '{0}'.format(date)
	elif(date>=0 or date<=10):
		return '0{0}'.format(date)
	else: 
		return '{0}'.format(date)