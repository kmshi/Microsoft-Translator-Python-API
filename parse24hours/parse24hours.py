from bs4 import BeautifulSoup,Tag,NavigableString
import urllib,codecs,os
from microsofttranslator import Translator

if os.path.exists('output'): shutil.rmtree('output')
os.makedirs('output/start-bg-pics')

soup = BeautifulSoup(open("24hours.htm"),'html5lib')

client_id = "translaterpythonapi"
client_secret = "FLghnwW4LJmNgEG+EZkL8uE+wb7+6tkOS8eejHg3AaI="
translator = Translator(client_id,client_secret)

current = 1
rSoup = BeautifulSoup("<xml></xml>")

ul_tag = soup.find_all("div",{"class":"gio carousel"})[0].ul
for a in ul_tag.find_all('a'):
    url = "http://www.guardian.co.uk/news/gallery/2012/jul/17/1" + a["href"]
    aSoup = BeautifulSoup(urllib.urlopen(url),'html5lib')
    
    imgurl = aSoup.find_all(id='main-picture')[0]["src"]
    caption = aSoup.find_all("span",{"class":"caption"})[0].string
    credit =  aSoup.find_all("span",{"class":"credit"})[0].string

    picpath = "output/start-bg-pics/"+str(current)+".jpg"
    filename, headers = urllib.urlretrieve(imgurl,picpath)
    if not filename.endswith(picpath): shutil.copyfile(filename,picpath)
    
    
    caption_cn = translator.translate(caption,'zh-CHS')
    
    cap_tag = rSoup.new_tag("caption")
    cap_tag["id"] = current
    
    
    en_tag = rSoup.new_tag("en")
    en_tag.string = caption
    cap_tag.append(en_tag)
    
    cn_tag = rSoup.new_tag("cn")
    cn_tag.string = caption_cn
    cap_tag.append(cn_tag)
    
    rSoup.xml.append(cap_tag);
    
    if current == 5 or current ==10:
        translator = Translator(client_id,client_secret)
        
    current = current +1

fp = codecs.open("output/result.xml", "w", "utf-8" )
fp.write(rSoup.prettify())
fp.close() 