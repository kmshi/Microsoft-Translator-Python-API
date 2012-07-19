from bs4 import BeautifulSoup,Tag,NavigableString
import urllib,codecs,os,sys,shutil,urllib2
from microsofttranslator import Translator

def parseGallery(gallery_url):
    if os.path.exists('output'): shutil.rmtree('output')
    os.makedirs('output/start-bg-pics')

    soup = BeautifulSoup(urllib2.urlopen(gallery_url),'html5lib')

    client_id = "translaterpythonapi"
    client_secret = "FLghnwW4LJmNgEG+EZkL8uE+wb7+6tkOS8eejHg3AaI="
    translator = Translator(client_id,client_secret)

    
    rSoup = BeautifulSoup("<xml></xml>")
    images = list()

    ul_tag = soup.find_all("div",{"class":"gio carousel"})[0].ul
    a_list = ul_tag.find_all('a')
    
    current = 1
    for a in a_list:
        url = gallery_url + a["href"]
        
        #htmpath = "output/x"+str(current)+".htm"
        #filename, headers = urllib.urlretrieve(url,htmpath)
        #if not filename.endswith(htmpath): shutil.copyfile(filename,htmpath)
        
        #aSoup = BeautifulSoup(open(htmpath),'html5lib')
        aSoup = BeautifulSoup(urllib2.urlopen(url),'html5lib')
    
        imgurl = aSoup.find_all(id='main-picture')[0]["src"]
        
        print str(current) + " url: " + url +"\n" 
        print str(current) + " imgurl: " + imgurl +"\n" 
        
        caption = aSoup.find_all("span",{"class":"caption"})[0].string
        credit =  aSoup.find_all("span",{"class":"credit"})[0].string
        if not isinstance(caption,basestring) : continue
        
        print str(current) + " caption: " + caption +"\n"
        print str(current) + " credit: " + credit +"\n"
        aSoup = None
        
        images.append(imgurl)
        caption_cn = translator.translate(caption,'zh-CHS')
        #caption_cn = "xxx"
    
        cap_tag = rSoup.new_tag("caption")
        cap_tag["id"] = current
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
        
        current = current +1
        

    rSoup.xml['total'] = len(a_list)
    fp = codecs.open("output/result.xml", "w", "utf-8" )
    fp.write(rSoup.prettify())
    fp.close()
    
    current = 1
    for imgurl in images:
        picpath = "output/start-bg-pics/"+str(current)+".jpg"
        filename, headers = urllib.urlretrieve(imgurl,picpath)
        if not filename.endswith(picpath): shutil.copyfile(filename,picpath)
        current = current +1

def main(args=sys.argv):
    if len(args) != 2:
        print "Usage: guardian_url\n"
        print "guardian_url: for example -- http://www.guardian.co.uk/news/gallery/2012/jul/17/1 \n"
        return 1
    else:
        parseGallery(args[1])

if __name__ == '__main__':
    sys.exit(main())
