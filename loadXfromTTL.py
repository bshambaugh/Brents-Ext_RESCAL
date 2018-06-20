# https://docs.python.org/2/library/fnmatch.html
import fnmatch
import os
from rdflib import Graph
from collections import defaultdict
from scipy.sparse import csr_matrix
from numpy import ones
from rfc3987 import parse

def loadXfromTTL(inputFile):
 g = Graph()
 g.parse(inputFile,format='ttl')


 triples = defaultdict(list)
# attributes = defaultdict(list)
 m = 0
# n = 0
 predobjstrlist = []
 #grab all of the predicates
 predicateList = []
 objectList = []
 subjectList = []
 for s, p, o in g:
    try:
      parse(o, rule='IRI')
      predicateList.append(p)
      objectList.append(o)
      subjectList.append(s)
#      print 'true', s , p , o
      triples[m].append(s)
      triples[m].append(p)
      triples[m].append(o)
      m = m + 1
    # I need to save the true predicates here
    except:
      print 'false', s, p, o
 #      attributes[n].append(s)
 #     pred = p.decode('UTF-8')
 #     obj = o.decode('UTF-8')
 #     predobj = pred + obj
 #     attributes[n].append(predobj)
 #     predobjstrlist.append(predobj)
     # I need to give the predicate - object a unique id
 #     attributes[n].append(p)
 #     attributes[n].append(o)
 #     n = n + 1

# But this code does not exclude subjects that lack any link to a URI object. I am not sure this is a necessity
 #print 'here is the attributes dictionary'
 #print attributes
 #print '================================='
 # match the attributes with the subject - object list ...

 # print 'here is the predicate object string list'
 # print predobjstrlist
 # print '================================='

 print 'here is the predicate list'
 print predicateList
 print '==========================='

 print 'here is the subjectlist =========='
 print subjectList
 print '=================================='


 print 'here is the objectlist ================'
 print objectList
 print '======================================='

 subObjList = subjectList+objectList

# Look to see if an object is a String..I suppose it is not a valid URL
 print '================start of subjObjList==================='
 print subObjList
 print '==============end of subjObjList============='

 # unique subject/object dictionary
 o = {}

 i=0
 for letter in subObjList:
    letter = letter.decode('UTF-8')
    if ( letter not in o.values() ):
       o[i] = letter
       i = i + 1

 print 'uniqe subject/object dictionary'
 print o
 print '================================'
   
 #unique predicate dictionary

 d = {}

 i=0
 for letter in predicateList:
       letter = letter.decode('UTF-8')
       if ( letter not in d.values() ):
          d[i] = letter
          i = i + 1

 print 'unique predicate list dictionary'
 print d
 print '=================================='

 rows = defaultdict(list)
 cols = defaultdict(list)

# make this look like the code under the subgraph comment
 for key, value in triples.items():
     k1 = 0
     k2 = 0
     k3 = 0
     subject = value[0].decode('UTF-8')
     print 'the subject is:', subject
     for k, v in o.items():
      if subject == v:
         k1 = k
         print 'k1 is:', k1  
     predicate = value[1].decode('UTF-8')
     print 'the predicate is:', predicate
     for k, v in d.items():
      if predicate == v:
         k2 = k
         print 'k2 is:', k2
     obj = value[2].decode('UTF-8')
     print 'the object is:', obj
     for k, v in o.items():
       if obj == v:
          k3 = k
          print 'k3 is', k3
     rows[k2].append(k1)
     cols[k2].append(k3)


 # I need to create a subgraph that I can work on to get X.T
# for subject, predicate, obj in g:
 #    k1 = 0 
 #    k2 = 0
 #    k3 = 0
 #    subject = subject.decode('UTF-8')
 #    print 'the subject is:', subject
 #    for k, v in o.items():
 #     if subject == v:
 #        k1 = k
 #        print 'k1 is:', k1
 #    predicate = predicate.decode('UTF-8') 
 #    print 'the predicate is:', predicate
 #    for k, v in d.items():
 #     if predicate == v:
 #        k2 = k
 #        print 'k2 is:', k2
 #    obj = obj.decode('UTF-8')
 #    print 'the obj is:' , obj
 #    for k, v in o.items():
 #      if obj == v:
 #         k3 = k
 #         print 'k3 is:', k3
 #    rows[k2].append(k1)
 #    cols[k2].append(k3)

 print 'rows: ',rows
 print 'cols: ',cols
 print 'the triples are: ',triples
 print 'the first one is:'
 #print triples[0][1]

 dim = len(o)
 X = []
# print len(rows[0])
 if len(rows) == len(cols):
   for key, value in rows.items():
       daones = ones(len(rows[key]))
       Xi = csr_matrix((daones,(rows[key],cols[key])), shape=(dim,dim))
       print Xi.toarray()
       X.append(Xi)
 return X

