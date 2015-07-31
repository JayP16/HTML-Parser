#!/usr/bin/env python2.7

import shutil
import cgi
import cgitb; cgitb.enable()
import sys
import os

print "Content-Type: text/html\n"

#os.seteuid(10017)
form = cgi.FieldStorage()
x = 0


while True:
    f = 'file[' + str(x) + ']'
    if f in form:
  	x = x + 1 
	filefield = form[f]
    	if not isinstance(filefield, list):
	    filefield = [filefield]

    	dir = "/var/www/vhosts/dev.applications.ene.gov.on.ca/httpdocs/jay/upload/to/" 
    	if not os.path.exists(dir):
            os.makedirs(dir)

    	for fileitem in filefield:
	    fn = dir + fileitem.filename
	    #print fn + "~~~~~~~~~~~~~~"
            # save file
	    f = open(fn, 'wb')
	    shutil.copyfileobj(fileitem.file, f)
	    f.close()
	
        #with open(fn, 'wb') as f:
        #    shutil.copyfileobj(fileitem.file, f)
    else:
	break
   
#f = open("version.txt", 'wb')
#data = sys.version
#f.write(data)
#f.close()
#shutil.rmtree(dir)
print dir.rstrip('/')
