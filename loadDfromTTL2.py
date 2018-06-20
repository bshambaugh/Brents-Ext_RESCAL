# https://docs.python.org/2/library/fnmatch.html
import fnmatch
import os
import numpy as np
from scipy.sparse import coo_matrix
from rdflib import Graph
from collections import defaultdict
from scipy.sparse import csr_matrix
from numpy import ones
from rfc3987 import parse

def loadDfromTTL(inputFile):
 g = Graph()
 g.parse(inputFile,format='ttl')


 triples = defaultdict(list)
 attributes = defaultdict(list)
 m = 0
 n = 0
 predobjstrlist = []
 #grab all of the predicates
 predicateList = []
 objectList = []
 subjectList = []
 for s, p, o in g:
    try:
      parse(o, rule='IRI')
#      predicateList.append(p)
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
      attributes[n].append(s)
      pred = p.decode('UTF-8')
      obj = o.decode('UTF-8')
      predobj = pred + obj
      attributes[n].append(predobj)
      predobjstrlist.append(predobj)
     # I need to give the predicate - object a unique id
 #     attributes[n].append(p)
 #     attributes[n].append(o)
      n = n + 1

# But this code does not exclude subjects that lack any link to a URI object. I am not sure this is a necessity
 print 'here is the attributes dictionary'
 print attributes
 print '================================='
 # match the attributes with the subject - object list ...

 print 'here is the predicate object string list'
 print predobjstrlist
 print '================================='

 # now I need a subj/obj dictionary to look up ids
 # I also need a pred/obj dictionary to look up ids
 uniqpredobjstr = {}
 l = 0
 for letter in predobjstrlist:
    letter = letter.decode('UTF-8')
    if ( letter not in uniqpredobjstr.values() ):
           uniqpredobjstr[l] = letter
           l = l + 1

 print 'here is the unique predicate object string'
 print uniqpredobjstr

 print 'here is the subjectlist'
 print subjectList
 print '=========================='

 print 'here is the objectlist'
 print objectList
 print '=========================='

 subObjList = subjectList + objectList

 o = {}
 i = 0
 for letter in subObjList:
    letter = letter.decode('UTF-8')
    if ( letter not in o.values() ):
       o[i] = letter
       i = i + 1

 print 'here is the subject-object dictionary'
 print o

 rows = defaultdict(list)
 cols = defaultdict(list)

 for key, value in attributes.items():
     print 'the key is', key, 'the subject is', value[0]
     k1 = 0
     k2 = 0
     subject = value[0].decode('UTF-8')
     print 'the subject is:', subject
     for k, v in o.items():
      if subject == v:
         k1 = k
         print 'k1 is:', k1 
     predobj = value[1].decode('UTF-8')
     print 'the predobj is', predobj
     for k, v in uniqpredobjstr.items():
      if predobj == v:
         k2 = k
         print 'k2 ks:', k2     
     rows[k1].append(k1)
     cols[k1].append(k2)

 print rows
 print cols

 dim = len(o)
 dim2 = len(uniqpredobjstr)
 D = coo_matrix((ones(6),(rows[0],cols[0])),shape=(dim,dim2),dtype=np.uint8).tocsr()

# dim = len(o)
# dim2 = len(uniqpredobjstr)
# D = []
# if len(rows) == len(cols):
#   for key, value in rows.items():
#       daones = ones(len(rows[key]))
#       Di = csr_matrix((daones,(rows[key],cols[key])), shape=(dim,dim2), dtype=np.uint8)
#       print Di.toarray()
#       D.append(Di)

 print D.toarray()
 return D

loadDfromTTL('oldfood.ttl')
