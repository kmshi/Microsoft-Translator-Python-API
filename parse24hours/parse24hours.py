from bs4 import BeautifulSoup,Tag,NavigableString
import urllib,codecs,os,sys,shutil,urllib2
from microsofttranslator import Translator
from urllib import FancyURLopener
from random import choice

user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
]

class MyOpener(FancyURLopener, object):
    version = choice(user_agents)

def retrievePage(url,current):
    myopener = MyOpener()
    htmpath = "output/x"+str(current)+".htm"
    #filename, headers = urllib.urlretrieve(url,htmpath)
    filename, headers = myopener.retrieve(url,htmpath)
    if not filename.endswith(htmpath): shutil.copyfile(filename,htmpath)

def retrieveImage(imgurl,current):
    myopener = MyOpener()
    picpath = "output/start-bg-pics/"+str(current)+".jpg"
    #filename, headers = urllib.urlretrieve(imgurl,picpath)
    filename, headers = myopener.retrieve(imgurl,picpath)
    if not filename.endswith(picpath): shutil.copyfile(filename,picpath)

def parseGallery(gallery_url):
    if os.path.exists('output'): shutil.rmtree('output')
    os.makedirs('output/start-bg-pics')

    retrievePage(gallery_url,'index');
    
    soup = BeautifulSoup(open('output/xindex.htm'),'html5lib')
    
    ul_tag = soup.find_all("div",{"class":"gio carousel"})[0].ul
    a_list = ul_tag.find_all('a')
    
    current = 1
    for a in a_list:
        url = gallery_url + a["href"]
        retrievePage(url,current)
        current = current + 1

    client_id = "translaterpythonapi"
    client_secret = "FLghnwW4LJmNgEG+EZkL8uE+wb7+6tkOS8eejHg3AaI="
    translator = Translator(client_id,client_secret)

    
    rSoup = BeautifulSoup("<xml></xml>")

    total = current -1
    current = 1
    while current <= total:
        imgurl = ""
        caption = ""
        credit = ""
        
        
        
        try:
            aSoup = BeautifulSoup(open('output/x'+str(current)+'.htm'),'html5lib')
            article_tag = aSoup.find_all("div",{"class":"article"})[0]
    
            imgurl = article_tag.find_all(id='main-picture')[0]["src"]
        
            print str(current) + " url: " + url +"\n" 
            print str(current) + " imgurl: " + imgurl +"\n" 
        
            caption = article_tag.find_all("span",{"class":"caption"})[0].string
            credit =  article_tag.find_all("span",{"class":"credit"})[0].string
        
            print str(current) + " caption: " + caption +"\n"
            print str(current) + " credit: " + credit +"\n"
            
            aSoup = None
            current = current +1
        except Exception as e:
            print e
            continue
            
        
        retrieveImage(imgurl,current -1)
        caption_cn = translator.translate(caption,'zh-CHS')
        #caption_cn = "xxx"
    
        cap_tag = rSoup.new_tag("caption")
        cap_tag["id"] = current -1
        cap_tag["credit"] = credit
        
        img_tag = rSoup.new_tag("img")
        img_tag['src'] = imgurl
        cap_tag.append(img_tag)
    
        en_tag = rSoup.new_tag("en")
        en_tag.string = caption
        cap_tag.append(en_tag)
    
        cn_tag = rSoup.new_tag("cn")
        cn_tag.string = caption_cn
        cap_tag.append(cn_tag)
    
        rSoup.xml.append(cap_tag);
    
        #if current == 5 or current ==10:
        #    translator = Translator(client_id,client_secret)
        
        
        

    fp = codecs.open("output/result.xml", "w", "utf-8" )
    fp.write(rSoup.prettify())
    fp.close()
 
 
def main(args=sys.argv):
    if len(args) != 2:
        print "Usage: guardian_url\n"
        print "guardian_url: for example -- http://www.guardian.co.uk/news/gallery/2012/jul/17/1 \n"
        return 1
    else:
        parseGallery(args[1])

if __name__ == '__main__':
    sys.exit(main())
