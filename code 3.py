# -*- coding: utf-8 -*-

"""
Created on Fri Sep 04 17:12:33 2015

@author: egon
"""
# audit street names
# save street types 
# and some street names for analysing it
# in Barcelona, street names are in the form:
# <street type> <street name>
# Ex.: Avenida Diagonal, Carrer de la Font, Plaça Catalunya

import xml.etree.cElementTree as ET
import pprint
import re
import csv


path="c:\\users\\egon\\desktop\\Data analysis udacity\\project 3\\"
filename=path+"barcelona_spain.osm"
  

street_types = {}
with_number = [] # save street names who have numbers in the end

def checkFile(filename):
    
        f = open(filename,'r')
        counter=0        
        
        for event,element in ET.iterparse(f):
            
            # print some output periodically
            if (counter % 100000)==0:
                print ".",
            counter += 1
            
            #check addr:street values
            if (element.tag=='tag') and (element.attrib['k']=='addr:street'): 
                   v = element.attrib['v']
                   
                   #is there a number in the end of street name?
                   r= re.search(" *, *\d+ *$",v)
                   if r:
                       with_number.append(v)
                       #print ">"+ v[0:len(v)-len(r.group())]+"<"
                   
                   #is there a "km" at the end ?
                   r= re.search(" *[Kk][Mm] *\.?\d+[.,]?\d+ *$",v)
                   if r:
                       with_number.append(v)
                       #print ">"+v[0:len(v)-len(r.group())]+"<"
                   
                   v = v.lower()
                   
                   #save street types
                   #street names are in format <streetformat> <name>
                   #ex: Carrer de la Font                  
                   strtype = v[0:v.find(' ')]
                   if strtype in street_types:                       
                       street_types[strtype]['count'] += 1
                   else:
                       street_types[strtype]={'count':1}
                                
            element.clear()  
       

def test():
    
    checkFile(filename)
        
    print ""
        
    #save data for analysis
        
    with open(path+'result3.txt', 'w') as results:
        pprint.pprint(street_types,results)
        pprint.pprint("",results)
        pprint.pprint(with_number,results)
        
    print "done"
    
  
test()
    

