#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, codecs, urllib2, re, urllib, shutil,os
from jinja2 import Template
from jinja2 import Environment, PackageLoader
from bs4 import BeautifulSoup

def generateDossier(env,dictObj):
    if (dictObj["current"]=="1"):
        template = env.get_template('start_html.template')
    else:
        template = env.get_template('html.template')
        
    #fp = open("log.txt","w")
    fp = codecs.open('output/'+ dictObj["current"] + ".html", "w", "utf-8" )
    fp.write(template.render(dictObj))
    fp.close()
    
def generateBookJson(env,book_title,contents):
    template = env.get_template('book.json.template')
    fp = codecs.open("output/book.json", "w", "utf-8" )
    fp.write(template.render({"title":book_title,"contents":contents}))
    fp.close()

def parseHTML(url,book_title):
    env = Environment(loader=PackageLoader('parsegen', 'templates'))
    #soup = BeautifulSoup(open("gardian/index.xhtml"),'lxml')
    soup = BeautifulSoup(open(url),'lxml')
    #soup.prettify()
    
    contents = list()
    
    for caption_tag in soup.find_all('caption'):
            title,description = caption_tag.cn.string.strip().split(u'：',1)
            current = caption_tag['id']
            total = caption_tag.parent['total']   
            source = "photograph:AP"
        
            #print "pic:" + url
            #print "title:" + title.encode("utf-8")
            #print "description:" + description.encode("utf-8")
            #print "total:" + total
            #print "current:" + current
            #print "source:" + source.encode("utf-8")
        
            dictObj = {"title":title,"description":description,"total":total,"current":current,"source":source}
            #print dictObj
                
            generateDossier(env,dictObj)
            
            contents.append(current + ".html")
        
            #break
        
    #print str(contents).replace('u','')
    generateBookJson(env,book_title,str(contents).replace('u','').replace("'",'"'))
    

def main(args=sys.argv):
    if len(args) != 2:
        print "Usage: issue_number\n"
        print "issue_number: for example -- 0001 \n"
        return 1
    else:
        shutil.copytree('fonts','output/fonts')
        shutil.copytree('images','output/images')
        shutil.copytree('inc','output/inc')
        shutil.copytree('js','output/js')
        shutil.copytree('styles','output/styles')
        
        book_title = u'环球'+ args[1]
        parseHTML("output/result.xml",book_title)
        

if __name__ == '__main__':
    sys.exit(main())

 
    
    





