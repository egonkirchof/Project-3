# -*- coding: utf-8 -*-
"""
Created on Fri Sep 04 17:12:33 2015

@author: egon
"""

# auditing addr:city for accuray
# based on the official list of cities for Barcelona region
# data is unicode (utf-8) so we have to do some conversion before
# comparing city in XML field with those in the list of cities

import xml.etree.cElementTree as ET
import pprint
import re
import csv


path="c:\\users\\egon\\desktop\\Data analysis udacity\\project 3\\"

filename=path+"barcelona_spain.osm"
cities="municipios barcelona.csv"

problems  = set()

def checkCity(filename):
    
        f = open(filename,'r')
        counter=0
        
        
        for event,element in ET.iterparse(f):
            
            # print some output periodically
            if (counter % 50000)==0:
                print ".",
            counter += 1
            
            #check if city in list of cities
            if (element.tag=='tag') and (element.attrib['k']=="addr:city"):
                #convert city in XML to string                
                val = element.attrib['v'].encode('utf-8').lower()                
                if val not in citiesBarcelona:                   
                    #if city not in citiesBarcelona save it                    
                    problems.add(val)
                    
            element.clear() # release some memory 


# read official list of cities for Barcelona province
# in CSV file

def read_cities():
    global citiesBarcelona
    
    citiesBarcelona = []
    
    with open(path+cities,'r') as f:
        creader = csv.DictReader(f)
        for r in creader:
           # pprint.pprint(r['NOMBRE']+" "+str(type(r['NOMBRE']) ))
            name = r['NOMBRE']
            name = name.lower()
            #pprint.pprint( name)
            if name.find(",")>-1:
                #some cities are in the format: Name, Prefix
                #like El Bruc = Bruc, El
                #so we add both formats
                #print name
                n,p = name.split(", ")
                if p.endswith("'"): # like in l´hospitalet
                    citiesBarcelona.append(p+n)  
                else: # like in la palma
                    citiesBarcelona.append(p+" "+n)     
                #sometimes the city appears withou its prefix
                #lets add it as a valid name
                #when we save to db we'll uniform it
                citiesBarcelona.append(n)
                
            citiesBarcelona.append(name)
        
       
        

def test():

    read_cities()
    print ""
    #pprint.pprint(citiesBarcelona)
    print "\n\n"    
    checkCity(filename)
    print ""
    
    #pprint.pprint(problems)
    
    #save cities not found in the list for analysis    
    with open(path+'result4.txt', 'w') as results:
        pprint.pprint(len(problems),results)
        pprint.pprint(problems,results)
        
    print "done"
  
test()
    