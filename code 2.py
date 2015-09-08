# -*- coding: utf-8 -*-
"""
Created on Fri Sep 04 17:12:33 2015

@author: egon
"""

# auditing phone, color, height/elt, addr:housenumber
# capacity/population, postcode fields for validity
# in this file we parse the XML and see if the values in the
# selected fields match some re we define
# if they don´t we print the values so we can analyse it lateer

import xml.etree.cElementTree as ET
import pprint
import re
import csv


path="c:\\users\\egon\\desktop\\Data analysis udacity\\project 3\\"

filename=path+"barcelona_spain.osm"


#create some functions for "pre treating" some fields
#like removing spaces in phone numbers
#so it will match simpler reg exps


def prePhone(value):
    #remove any space between digits
    res = ""
    for c in value:
        if c not in " # .-()+":
            res = res + c
    return res
    
#create some regexps to validate target fields          
# fields we want to check for validity
# if the fields content doesn´t match a regexp we output it

          
valTable = [ { 'fields' :['addr:postcode'], 'res' : [ "^08[0-9]{3}$" ] },
             { 'fields' : ['phone','fax','contact:fax','contact:phone'],
                'res': [ "^(\+?34)?[679]\d{8}$"], 'pre':prePhone},
             {'fields': ['ele','building:height','roof:height','height'] ,
                 'res' : [ '^ *\+?\d*(\.|\,)?\d+( ?m.?)?$' ]} ,
             {'fields': ['capacity','population']  , 'res': ['^\ *\d+ *$']} ,
             {'fields': ['addr:housenumber'],'res':["^\d+$",'^km ?\d+\.?\d+'\
                     ,"^\d+ *\w$","^\d+( *[-;, ] *\d+)*\w?$","^(sn)|(s/n)$" ]}]

problems  = {} 

def checkValues(filename):
    
        #for a list of "keys" in tags
        #check if value matches a regular expression
    
        f = open(filename,'r')
        counter=0
        
        
        for event,element in ET.iterparse(f):
            
            # print some output periodically
            if (counter % 100000)==0:
                print ".",
            counter += 1
            
            if (element.tag=='tag'): 
                k = element.attrib['k']
                
                # look for fields we want to validate
                for it in valTable:
                    if k in it['fields']:
                        exprList = it['res']
                        ok = False
                        val = element.attrib['v']               
                        if 'pre' in it:
                            val = it['pre'](val)
                    
                        #value matches any re for that field?
                        for expr in exprList:
                            #print expr
                            if re.search(expr,val):
                                ok = True
                                break
                    
                        #save values that don´t match
                        if not ok:
                            if k in problems:
                                problems[k].append(element.attrib['v'])
                            else:
                                problems[k] = [element.attrib['v']]
                                
                        break # no need to continue for loop
                        
            element.clear() #release some memory
            

def test():
    
    checkValues(filename)
    
    print ""
    
    #pprint.pprint(problems)
    
    # save info in file for analysis
        
    with open(path+'result2.txt', 'w') as results:
        pprint.pprint(problems,results)
        pprint.pprint("",results)
  
    print "done"
    
test()
    

