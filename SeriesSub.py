import urllib.request
#import urllib2
import requests
import zipfile
import os
import shutil
from bs4 import BeautifulSoup

from google import search


series = input("Enter series to be searched: \n")

 #I am feeling lucky of duckduckgo

#url = "https://duckduckgo.com/?q=!ducky+tv+subtitles+"+series+"+show"

'''
opener = urllib.request.build_opener()
request = urllib.request.Request(url)
u = opener.open(request)
finalurl = u.geturl()
'''

#finalurl = urllib.request.urlopen(url).geturl()

'''
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
   finalurl = response.url()
'''

#parse specific season details using beautifulsoup
'''
r = requests.get(url)
#response = requests.get(r.url)
soup = BeautifulSoup(r.text, "html.parser")
start = str(soup.contents).find("uddg=")+5
end = str(soup.contents).find('html"')
finalUrl = str(soup.contents)[start:end]
'''

#The below is one method
finalurl=''
for url in search('insite: tvsubtitles.net ' + series + ' show', stop=1,num=2):
        finalurl = url
        break
print(finalurl)


r = requests.get(finalurl)
#response = requests.get(r.url)
soup = BeautifulSoup(r.text, "html.parser")
myP = soup.findAll("p", { "class" : "description" })
#print((soup.contents))
print (myP)
myP = str(myP)

subURLList = []

start = finalurl.find("tvshow") + 6
end = finalurl.find("html")-1
subURLList.append(finalurl[start:end])

start = 1
while (start!=11): #check next step; when start is -1 , it actually becomes 11
    start = myP.find("href=") + 6 + 6 #for passing over 'tvshow'
    end = myP.find("html")-1

    subURLList.append(myP[start:end])
    end+=5
    myP = myP[end:]

if not os.path.exists('tempSubs'):
    os.makedirs('tempSubs')

i=1
for k in subURLList:
    print (k)
    try:
        urllib.request.urlretrieve ("http://www.tvsubtitles.net/download" +k+"-en.html", "tempSubs\\" + str(i) + ".zip")
        zip_ref = zipfile.ZipFile("tempSubs\\" + str(i) + '.zip', 'r')
        zip_ref.extractall("tempSubs\\")
        zip_ref.close()
    except:
        print("error")
    i+=1




dialogue = input("Enter dialogue to be searched: \n")

resultList = []

for filename in os.listdir('tempSubs'):
    if dialogue in open('tempSubs\\' + filename).read():
        resultList.append(filename)

if os.path.exists('tempSubs'):
    shutil.rmtree('tempSubs')
    #os.remove('tempSubs')
    #os.removedirs('tempSubs')

print("The episodes in which entered dialogue occurs are: " + str(resultList))

