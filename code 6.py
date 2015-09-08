# -*- coding: utf-8 -*-
"""
Created on Sun Sep 06 20:14:51 2015

@author: egon
"""

### querying our collection 
### in this file we query our mongodb using a function q()
### we save the results in a file so we can put it in our report more easily


from pymongo import MongoClient
import pprint as pp

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

path="c:\\users\\egon\\desktop\\Data analysis udacity\\project 3\\"

output=path+"result6.txt"


def q(description,pipeline):
    
    print "Query: ",description,"\n" 
    pp.pprint( pipeline )
    print ""
    
    pp.pprint("Query: "+description,fileout)
    pp.pprint(pipeline,fileout)
    pp.pprint("",fileout)
    
    result = db.map.aggregate(pipeline)
    
    pp.pprint(result['result'])
    print "\n\n"
    
    pp.pprint(result['result'],fileout)
    pp.pprint("",fileout)
    pp.pprint("",fileout)
    
    return result['result']
    
def q_basic():
    
    q( "# of documents",
         [ {"$group": {"_id": None, "count": {"$sum":1}}}  ] )
 
   
    q( "# of 'nodes'",
      [ { "$match":{"element_type":"node"}} ,
         {"$group": {"_id":"$element_type", "count": {"$sum":1}}}   ] )

    q( "# of 'ways'",
      [ { "$match":{"element_type":"way"}},
         {"$group": {"_id":"$element_type", "count": {"$sum":1}}}   ] )
         
    q( "# of unique users",
      [
         {"$group": {"_id":"$created.user", "count": {"$sum":1}}},
        {"$group": {"_id":None, "count": {"$sum":1}}}    ] )

    q( "top five users",
      [
         {"$group": {"_id":"$created.user", "count": {"$sum":1}}},
        {"$sort": {"count": -1}}, { "$limit": 5}     ] )
    
    q( "top five amenities",
      [  { "$match": { "amenity": {"$exists":1}}} ,
         {"$group": {"_id":"$amenity", "count": {"$sum":1}}},
        {"$sort": {"count": -1}}, { "$limit": 5}     ] )


def barG(results,bins,title,xlabel,ylabel,filename):
# create bar graph with result from a query
# the result contains "_id" and "count"
# count is sorted
# we put each element in a range and count 

    binsLabels=[]
    prev = 1
    for i in bins:
        it = str(prev)+"-"+str(i)
        prev = str(i)
        binsLabels.append(it)

    # results are already sorted by count
    idx = 0
    binsCount = [0]*len(bins)
    for it in results:        
        if (it['count']> bins[idx]) and (idx<(len(bins)-1)):
            idx += 1            
        binsCount[idx] += 1 
       
    r = range(len(binsLabels))
    
    f={'family' : 'Sans Serif', 'weight' : 'bold','size'   : 20}
    mpl.rc('font', **f)
    
    plt.figure(figsize=(18,18))
    plt.bar(r, binsCount,align='center')
    plt.xticks( r, binsLabels,rotation=45)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(path+filename)
    
    
def queries():
    global fileout,db
    
    client = MongoClient('localhost:27017')
    db = client["barcelona"]
    fileout = open(output,'w')

    q_basic()

    r = q( "# amenities per city",
      [  { "$match": {"amenity":{"$exists":1},"address.city":{"$exists":1}}} ,
         {"$group": {"_id": {"acity":"$address.city","amenity":"$amenity"}, "count": {"$sum":1}}},
         {"$sort": {  "_id.amenity": 1, "_id.acity":1  }}
        ] )
 
    
    # used for generating a bar graph
    r = q( "#contributions per users",
      [
         {"$group": {"_id":"$created.uid", "count": {"$sum":1}}},
        {"$sort": {"count": 1}}     ] )
    
    # barG(r,[10,100,1000,10000,100000],"User contributions", "# of contributions","# of users","figure q1.jpg")

    fileout.close()
    client.close()
    
    print "done"
    
queries()
