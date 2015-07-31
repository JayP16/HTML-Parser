#!/usr/bin/env python

from bs4 import BeautifulSoup
import sys
import os
import urllib2
import urllib
from urlparse import urljoin
import shutil
import cgi
import cgitb; cgitb.enable()

class HTMLPARSER:
    
    headers = ['h1','h2','h3','h4','h5', 'h6']	
    keepTags = ['a','ul','ol','figure','strong','img','p','table','caption','th','tr','td','li','dl','dt']   
    imagesLocation = 'www.dev.applications.ene.gov.on.ca/dams/images/'
    docsLocation = 'http://www.dev.applications.ene.gov.on.ca/dams/Docs/'

    def __init__(self, file_name):
        
        self.file = file_name
        #self.soup = BeautifulSoup(open(file_name), "lxml")
        self.soup = BeautifulSoup(open(file_name), "html.parser") 
        #print self.soup.prettify("utf-8")
	self.string = ''       
	self.toc = None
	self.id = file_name.split('/')[-1].split('-')[0]
	self.lastHeaderIndex = 0
	self.lastHeaderObj = {'h1':None, 'h2':None,'h3':None, 'h4':None, 'h5':None, 'h6':None}

 
    def prettify(self):
        html = self.soup.prettify("utf-8")
        with open(self.file, "wb") as file:
            file.write(html)
        file.close()

    def header(self):
	title =  self.soup.find('h1')
	self.string += str (title)
	self.lastHeaderIndex = self.headers.index(title.name)
	print self.lastHeaderIndex 
	
	
	#print title.contents
	#print title.prettify()
	self.get_contents(title.next_sibling)
	 
	while (title.parent != None and title.parent.next_sibling != None):
	    title = title.parent.next_sibling
	    inside = title
	    #print inside.contents 
	    
     	    while (inside.next_sibling != None):
	        try:
	            print "1 <br />" + title
	            for child in inside.contents:
	    	        print "child ...." + child + "<br />"
	    	    	self.get_contents(child)
		except:
		    self.string += str(title)
		    print "in except <br />"

       	   # print vars(title)

    def get_contents(self, contents):
	contents = contents.next_sibling
	while (contents != None):
	    print "=====================" + str(contents) + "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	    self.string += str(contents)
	    contents = contents.next_sibling

    def DFS(self):
	parent = None
	current = None
	toc = None

	#change anchor links to documents
 	self.change_doc_ref()

	#change image tag links
	self.change_image_source()

        for child in self.soup.recursiveChildGenerator():
     	    #print "(((((((((((((((((" + self.string + ")))))))))))))))))"
	    name = getattr(child, "name", None)
     	    if name is not None :
		if name in self.keepTags and self.check_parents(child):
		   # if name == 'a':
		#	if self.aTag(child):
		#	    self.string += child.prettify('utf-8')
		 #   else:
		    self.string += child.prettify('utf-8')
		#tag is one of the header tags
		if name in self.headers:
		    toc = TOC(child, current)
	 	    self.lastHeaderObj[name] = toc
		    self.lastHeaderIndex = self.headers.index(name)
		    if name != 'h1':
			#print "~~~~~~~~~~~~~~~~~~~~~~+++++++++++++++++++++++++++++++++++++++++++++++++"
			#print self.string
			current.add_content(self.string)
			self.string = ''
			self.lastHeaderObj[self.headers[self.headers.index(name) - 1]].insert(toc)
			parent = current
			#parent.insert(toc)
		    current = toc 
		    #self.string +=  child.prettify('utf-8')
		          
  	    elif not child.isspace(): # leaf node, don't print spaces
                if child.parent.name not in self.headers and self.check_parents(child) and self.lastHeaderObj['h1'] != None:
		    self.string += child.encode('utf-8')
	toc.add_content(self.string)
	self.toc = toc

    def build_TOC(self):
	tocStr = ''
	for child in self.soup.recursiveChildGenerator():
	    name = getattr(child, "name", None)
	    if name is not None and name in self.headers:
		tocStr +=  child.prettify('utf-8')
	return tocStr

    def aTag(self, tag):
	for x in tag.parents:
	    if x.name in self.headers:
		return False
	return True

    def check_parents(self, tag):
	for x in tag.parents:
	    if x.name in self.keepTags:
		return False
	return True

    def print_inorder(self, index, pid = 0):
	#print indent, index.title	
	tags = ["<"+x+">" for x in self.keepTags]
	tags = ' '.join(tags)
	data = {'assetId': self.id, 'title':index.title,'data':index.content, 'pid': str(pid), 'keepTags':tags}
	req = HTTP()
	req.post_data(data) 
	if (pid == 0):
	    req.delete_existing()
	    
	#print "<br />vvvvvvvvvvvvvvvvvvvvvvv<br />" + index.title.text + "<br />" + index.content + "<br /> ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^~<br />" 
	pid = int(req.send_request())
	
	for x in index.child:
	    self.print_inorder(x, pid)
  
    def change_doc_ref(self):
	for x in self.soup.findAll('a'):
	    if x.has_attr('href') and x['href'].count("Docs/"):
		x['href'] = self.docsLocation + x['href'].split('/')[-1]

    def change_image_source(self):
	for x in self.soup.findAll('img'):
	    x['src'] = self.imagesLocation + x['src'].split('/')[-1]
	    #new = self.soup.new_tag("img")
	    #new['src'] = x['src']
	    #new['alt'] = x['alt']
	    #new.attrs = x.attrs
	    #x.replace_with(new) 

class Tags:
    def __init__(self, tag):
	self.tag = tag

class TOC:
    
    def __init__(self, title, parent = None):
	self.title = title
	self.content = ''
	self.child = []
	self.parent = parent

    def insert(self, sub):
	self.child.append(sub)

    def add_content(self,string):
	self.content = string

class HTTP:
    """
    Responsible for POST requests. For all requests set either 'insert' or 'delete' variable.

    Eg. To delete data of a particular asset
              data = {'delete': id}
 
        To insert/upadte a asset
	      data = {'insert': id, 'title': title, 'data':data, ... } 
    """

    base_url = "http://www.dev.applications.ene.gov.on.ca/dams/import/"
    import_func = "importExisting" 
    delete_func = "deleteSections"
  
    def __init__(self):
	self.data = {}

    def post_data(self, data):
	self.data = data

    def send_request(self):
	path = self.base_url + self.import_func
	data = urllib.urlencode(self.data)
	req = urllib2.Request(path, data)
	response = urllib2.urlopen(req)
	html = response.read()
	return html.split('id:')[1].split(':id')[0]	

    def delete_existing(self):
	path = self.base_url + self.delete_func 
	data = urllib.urlencode(self.data)
	req = urllib2.Request(path, data)
	response = urllib2.urlopen(req)

def directory(dir):
    for filename in os.listdir(dir):
        if (os.path.isfile(dir + "/" + filename)):
            single_file(dir + "/" + filename)
        elif os.path.isdir(dir + "/" + filename):
            directory(dir + "/" + filename)
    

def single_file(file_name):
    x = HTMLPARSER(file_name)
    #print file_name.split('-')[0]
    #x.prettify()
    #x.build_TOC()
    #print file_name
    x.DFS()
    #x.change_image_source()
    #x.change_link_ref()
    x.print_inorder(x.lastHeaderObj['h1'])

if __name__ == "__main__":
    files = sys.argv[1]
    if (os.path.isfile(files)):
	single_file(files)
	os.remove(files)
    elif os.path.isdir(files):
        directory(files)
	shutil.rmtree(files)
