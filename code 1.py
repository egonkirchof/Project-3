
# -*- coding: utf-8 -*-

"""
Created on Fri Sep 04 17:12:33 2015

@author: egon
"""

# parse the XML to see how many distinct tags we have 
# which attribs they have
# get all distinct "keys" for tag "tag"
# and also some examples for "v" values 

import xml.etree.cElementTree as ET
import pprint
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

path="c:\\users\\egon\\desktop\\Data analysis udacity\\project 3\\"

filename=path+"barcelona_spain.osm"

keys = {} # save all distinct 'k' values in "tags"

def count_tags(filename):
        # YOUR CODE HERE
        dic = {}
        f = open(filename,'r')
        counter=0
                
        for event,element in ET.iterparse(f):
            
            # print something from time to time
            if (counter % 50000)==0:
                print ".",
            counter += 1
            
            
            if element.tag=='tag':
                
                k=element.attrib['k']
                # save all "k" found
                if k in keys:
                    keys[k]['count'] += 1
                    # save some samples of "v" values
                    if (keys[k]['count']%20)==0:
                        keys[k]['samples'].add(element.attrib['v'])
                else:
                    keys[k]={'count':1,'samples': set([element.attrib['v'] ]) }
                
            # save all tags found
            if element.tag in dic:             
                dic[element.tag]['count'] += 1
            else:             
                dic[element.tag] = {'count':1,'attribs':{} }   
            
            # save tag's attributes
            for a in element.attrib.keys():
                if a in dic[element.tag]['attribs']:
                    dic[element.tag]['attribs'][a] += 1
                else:
                    dic[element.tag]['attribs'][a] = 1
            
            element.clear() # for conserving memory
            

        return dic
    

# check what are the most frequent "ks"
# also see how many k'count are in each of the following ranges

bins = [10,20,50,100,200,500,1000,2000,5000,7000,10000,50000,100000]
binsLabels=["<10","<20","<50","<100","<200","<500","<1000","<2000","<5000","<7000","<10000","<50000","<100000"]


def mostFrequent(n):
    global x,t
    
    x =[]
    ks = keys.keys()
    copy = []
    binsCount = [0]*len(bins)
    
    for k in ks:
        c =  keys[k]['count']
        x.append(c)
        copy.append(c)
        #lets see in wich range # of this k falls into
        for i, b in enumerate(bins):
            if c<=b:
                binsCount[i] += 1
                break
            
    print "mean 'k':", np.mean(x)
    #print bins
    #print binsCount
    
    # find the n most frequent "ks"
    x.sort(reverse=True) # here are the count of occurrences
    t = [] # here goes the "k"
    
    for i in x[0:n]:
        idx= copy.index(i)
        t.append( ks[idx] )
        
    #print t
    #print x[0:n]
    
    return t,x[0:n],binsCount


# create a bargraph for 'k value' counts
def barGraph(binsCount):        
       
    r = range(len(binsLabels))
    
    f={'family' : 'Sans Serif', 'weight' : 'bold','size'   : 24}
    mpl.rc('font', **f)
    
    plt.figure(figsize=(15,15))
    plt.bar(r, binsCount,align='center')
    plt.xticks( r, binsLabels,rotation=45)
    plt.title("K attrib by occurences count")
    plt.xlabel("max # occurrences")
    plt.ylabel("number of k attribs")
    plt.savefig(path+'bar graph1.jpg')
    
    

    
def test():
    tags = count_tags(filename)
        
    print ""
    print len(tags)
    
    
    
    names,values,bCount = mostFrequent(10)
    barGraph(bCount)
    
    # save data about the file for analysis
    
    with open(path+'result1.txt', 'w') as results:
        pprint.pprint(len(tags),results)
        pprint.pprint(tags,results)
        pprint.pprint("",results)
        pprint.pprint("Distinct k/v pairs:",results)
        pprint.pprint(len(keys),results)
        pprint.pprint(keys,results)
        pprint.pprint("",results)
        pprint.pprint("Most frequent k/v pairs:",results)
        pprint.pprint(names,results)
        pprint.pprint(values,results)
        pprint.pprint("",results)
        pprint.pprint("K counts in ranges:",results)
        pprint.pprint(bins,results)
        pprint.pprint(bCount,results)

    print "done"
  
test()
    

