# -*- coding: utf-8 -*-
"""
Created on Sun Sep 06 11:47:07 2015

@author: egon
"""

# in this file we clean our data and export it as a json file
# so we can import it to mongodb later using mongoimport

import xml.etree.cElementTree as ET
import pprint
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import re
import codecs
import json

problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


path="c:\\users\\egon\\desktop\\Data analysis udacity\\project 3\\"
filename=path+"barcelona_spain.osm"


#some function to clean fields of interest before importing to db

def cleanPhone(value):
    # return 9 digits phone numbers without international code
    # or other chars like (34) or +34
    # also get the first number if there is a list of numbers

    value = value.replace(" ","")
    value = value.replace(".","")
    value = value.replace("-","")
    value = value.replace("(","")
    value = value.replace(")","")
    
    r = re.search("\d+",value)   
    if r:
        value = r.group()
        if value[0:2]=="00":
            value = value[2:]
        if value[0:2]=="34":
            value = value[2:]
        if len(value) < 9: # phones have 9 digits 
            return None
        return value[0:10]            
    else:
        return None
            
def cleanCapacity(value):
    #capacity should be an integer number
    r = re.search("^\d+",value)
    if r:
        return int(r.group())
    else:
        return None

def cleanEle(value):
    # elevation should be a float 
    r = re.search("^\d+[.,]?(\d+)?",value)
    if r:
        value = r.group().replace(",",".")        
        return float(value)
    else:
        return None
        
def cleanHouseNumber(value):
    #get only number part of housenumber
    r = re.search("^\d+",value)
    if r:
        return int(r.group())
    else:
        return None
    
def cleanPostCode(value):
    # there are a few problematic post codes
    # we use a table and return the right post code

    problems = {'72':'','08037 BCN':'08037', '089809':'',
                   '08':'08001', '8007': '08007', 'Barcelona':'08001'}
                   
    if value in problems:
        return problems[value]
    
    else:
        return value

# table for uniforming str types based on auditing we performed on street names
strtype_replace = { u'Carrer': ['c','c.','c/','cr'],
                    u'Avinguda' : ['av.','av','avda','avda.'],
                    u'Calle': ['cl'],
                    u'Carretera':['cra.','ctra.','crta.','ctra'],
                    u'Plaça': ['pl','pla','pl.'],
                    u'Passatge':['pg','pg.','pasatge'],
                    u'Rambla': ['rbla','rbla.']}     

def cleanStreet(value):
    # remove number or 'km' at the end of street name
    r= re.search(" *, *\d+ *$",value)
    if r:
        value = value[0:len(value)-len(r.group())]
    r= re.search(" *[Kk][Mm] *\.?\d+[.,]?\d+ *$",value)
    if r:
        value = value[0:len(value)-len(r.group())]
    
    # try to uniform str type base on auditing results 
    strtype = value[0:value.find(' ')].lower() # in spanish, street type comes before street name

    for k in strtype_replace.keys():
        if strtype in strtype_replace[k]:
            #print "("+strtype+")",
            value = k+value[value.find(' '):]
            #print value
                     
    return value
    
def cleanCity(value):
    # some cities are not in the oficial list of cities
    # so we ignore them
    value = value.encode('utf-8')    
    
    problems = ['08005', 'bellaterra', 'bellvitge', 'cerdanyola del valles',
     'el prat del llobregat barcelona','gava',  'gav\xc3\xa0 mar',
     "l'hospitalet de llobregat, barcelona",  'mira-sol. sant cugat del vall\xc3\xa8s',
     'sant adri\xc3\xa0 de bas\xc3\xb2s',     'sant adri\xc3\xa0 de besos',
     'sant adri\xc3\xa0 del bes\xc3\xb2s',    'sant cugat de vall\xc3\xa9s',     'sant cugat del vall\xc3\xa9s',
     'santa coloma de gramanet',    'santa perpetua de moguda',    'valldoreix, sant cugat del vall\xc3\xa8s']

    if value in problems:
        return None
    else:
        return value
        

k_to_clean = ["phone","capacity","ele","addr:housenumber","addr:postcode","addr:street","addr:city" ]
clean_procedure = [ cleanPhone, cleanCapacity,cleanEle,cleanHouseNumber,cleanPostCode,cleanStreet,cleanCity]



CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def get_attribs(node,element):    
        for k in element.attrib.keys():
            if k in CREATED:
                if 'created' not in node:
                    node['created']= {}
                node['created'][k] = element.attrib[k]
            elif k=="lat":
                if 'pos' not in node:
                    node['pos']=[0,0]
                node['pos'][0]=float(element.attrib[k])
            elif k=='lon':
                if 'pos' not in node:
                    node['pos']=[0,0]                
                node['pos'][1]=float(element.attrib[k])
            else:
                node[k] = element.attrib[k]
        
        
def shape_element(element):
    
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE
        node = { "element_type": element.tag }
        get_attribs(node,element)
        
        for sub in element:      
            if sub.tag=="tag":
                k = sub.attrib['k'].lower()
                
                if k=='address': # ignore field address (occurrs 1 time)
                    continue
                
                if problemchars.search(k):
                    continue
                
                v = sub.attrib['v'].strip()
                
                if k in k_to_clean:
                    clean = clean_procedure[k_to_clean.index(k)](v)
                    #print "clean ",k," :",v
                    if not clean:
                        pprint.pprint("rejected "+k+":"+v,outputfile)    
                        continue
                    v=clean

                if k.startswith("addr:"):
                    k = k[5:].strip()
                    if k.find(":")>0:
                        continue
                    if 'address' not in node:
                        node['address'] = {}
                    node['address'][k]=v
                else:
                    node[k] = v
            
            if sub.tag=="nd":
                if 'node_refs' not in node: 
                    node['node_refs'] = []
                node['node_refs'].append(sub.attrib['ref'])
            
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    
    file_out = "barcelona.json"
    data = []
    counter = 1
    previous = None
    docsCreated = 0
    
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):

            # print some output periodicly
            if (counter % 50000)==0:
                print ".",
                
            counter += 1
            
            el = shape_element(element)
            
            if previous:
                # for some reason you can't release the current element
                # only after getting the next one you can release the previous one
                previous.clear() # release some memory
            previous = element    
            
            if el:
                # data.append(el)
                # continue
                docsCreated += 1                
            
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
             
    print "Documents created:",docsCreated            
    return data

def test():
    global outputfile
          
    outputfile= open(path+'result5.txt', 'w') 
    data = process_map(filename)
    outputfile.close()
    print ""
    print "done"
    #pprint.pprint(data)

test()