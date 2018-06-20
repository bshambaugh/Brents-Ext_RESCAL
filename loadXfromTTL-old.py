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

 #grab all of the predicates
 predicateList = []
 for s, p, o in g:
    try:
      parse(o, rule='IRI')
      predicateList.append(p)
      print 'true'
    except:
      print 'false', p, o
 
 print 'here is the predicate list'
 print predicateList
 print '==========================='

 # grab all of the subjects
 subjectList = []
 for s, p, o in g:
    subjectList.append(s)

 print 'here is the subjectlist =========='
 print subjectList
 print '=================================='

 #grab all of the objects
 objectList = []
 for s, p, o in g:
    try:
      parse(o, rule='IRI')
      print 'true', o
      objectList.append(o)
    except:
      print 'false', o

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
   
 #unique predicate dictionary

 d = {}

 i=0
 for letter in predicateList:
       letter = letter.decode('UTF-8')
       if ( letter not in d.values() ):
          d[i] = letter
          i = i + 1


 rows = defaultdict(list)
 cols = defaultdict(list)

 for subject, predicate, obj in g:
     k1 = 0 
     k2 = 0
     k3 = 0
     subject = subject.decode('UTF-8')
     for k, v in o.items():
      if subject == v:
         k1 = k
     predicate = predicate.decode('UTF-8') 
     for k, v in d.items():
      if predicate == v:
         k2 = k
     obj = obj.decode('UTF-8')
     for k, v in o.items():
       if obj == v:
          k3 = k
     rows[k2].append(k1)
     cols[k2].append(k3)

# print 'rows: ',rows
# print 'cols: ',cols

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

