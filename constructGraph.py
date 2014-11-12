 #-*- coding: utf-8 -*-
import functools
import os
from snap import *
import linecache
path = os.getcwd()
def add(x,y): return x+'/'+y
path = functools.reduce(add,path.split('/')[:-1])
name = "amazon-meta.txt"
name = '/'+name
f = open(path+name, 'r')

#~ str = "similar: 5 1559360968 1559361247 1559360828 1559361018 0743214552"
#~ print(map(int,str.split(':')[-1].split()[1:]))
class Reviews : #all reviews
	def __init__ (self,file):
		line = file.readline().replace('\n','').replace('\r','')
		line = line.split('avg rating:')
		self.avgRating = float(line[-1])
		line = line[0].split('downloaded:')
		self.dowloaded = int(line[-1])
		line = line[0].split('total:')
		self.nb = int(line[-1])
		self.reviews = []
		for i in range(self.dowloaded) :
			line = file.readline()
			self.reviews.append(Review(line))
class Review : #one single review
	def __init__(self,line) :
		line = line.split('helpful:')
		#~ print(line[-1])
		self.helpful = int(line[-1])
		
		line = line[0].split('votes:')
		self.votes = int(line[-1])
		
		line = line[0].split('rating:')
		self.rating = int(line[-1])
		
		line = line[0].split('cutomer:')
		self.customer = line[-1]
		
		self.date = line[0].replace(' ','')
class Categories : #all categories
	def __init__(self,file):
		nb = int(file.readline().split(':')[-1])
		self.categories = []
		for i in range(nb):
			line  = file.readline()
			self.categories.append(Categorie(line))
class Categorie : #one single categorie
	def __init__(self,line):
		self.line = line
class Similars : #all similar product
	def __init__(self,line):
		splitted = line.replace('\n','').replace('\r','').split('similar:')[-1].split('  ')
		self.number = int(splitted[0])
		self.similar = []
		for i in range(self.number):
			self.similar.append(splitted[i+1])
		
class MyNode :
	def __init__(self,file) :
		self.Id  = int(file.readline().split(':')[-1])
		#~ print self.Id
		self.ASIN = file.readline().split(':')[-1]
		#~ print self.ASIN
		self.title = file.readline().split('title:')[-1]
		if  'discontinued product' in self.title  :
			return
		else :
			#~ print self.title
			self.group = file.readline().split('group:')[-1]
			#~ print self.group
			self.salesrank = file.readline().split('salesrank:')[-1]
			#~ print self.salesrank
			self.similars = Similars(file.readline())
			#~ print self.similar.similar
			self.categories = Categories(file)
			self.reviews = Reviews(file)
			file.readline()
		#~ for re in self.reviews.reviews :
			#~ print re.date
for i in range(7) : #remove the first useless lines
	f.readline()
a = []
while(1) :
	#~ try :
		a.append(MyNode(f))
	#~ except :
		#~ break
		
#~ id = 0
G1 = TNEANet.New()
#~ dic = {}
#~ intId = 1
#~ idNode = intId
#~ for line in f:
	#~ line = line.replace('\r','').replace('\n','')
	#~ if line[0:4] == 'ASIN' :
		#~ id = line.split(':')[-1]
		#~ if not(id in dic):
			#~ dic[id] = intId
			#~ G1.AddNode(intId)
			#~ intId += 1
		#~ idNode = dic[id]
	#~ if(line[0:9] ==  "  similar"):
		#~ try :
			#~ def addEdge(x):
				#~ if not(x in dic):
					#~ global intId
					#~ dic[x] = intId
					#~ G1.AddNode(intId)
					#~ intId +=  1
				#~ G1.AddEdge(idNode,dic[x] )
			#~ li = line.split(':')[-1].split()[1:]
			#~ map(addEdge,line.split(':')[-1].split()[1:])			
		#~ except :
			#~ pass
counter = 0
ff = open(path+name, 'r')
out = open(path+"/first100", 'w')
for line in ff:
	out.write(line)
	if(counter > 5000) :
		break
	counter += 1
ff.close()
out.close()
print G1.GetNodes()
print G1.GetEdges()

f.close()

#~ out.close()
#http://snap.stanford.edu/snappy/doc/reference/graphs.html#TNEANet for more informations
















#~ FIn = TFIn(path+name)
#~ G = TNGraph.Load(FIn)
#~ for NI in G.Nodes():
	#~ print "node id %d with out-degree %d and in-degree %d" % ( NI.GetId(), NI.GetOutDeg(), NI.GetInDeg())



#~ CntV = TIntPrV()
#~ # generate a Preferential Attachment graph on 1000 nodes and node out degree of 3
#~ G8 = GenPrefAttach(1000, 3)
#~ # vector of pairs of integers (size, count)
#~ CntV = TIntPrV()
#~ # get distribution of connected components (component size, count)
#~ print GetWccSzCnt(FIn, CntV) 
#~ # get degree distribution pairs (degree, count)
#~ print GetOutDegCnt(FIn, CntV)
#~ # vector of floats 
#~ EigV = TFltV() 
#~ # get first eigenvector of graph adjacency matrix 
#~ print GetEigVec(FIn, EigV) 
#~ # get diameter of FIn 
#~ print GetBfsFullDiam(FIn, 100) 
#~ # count the number of triads in FIn, get the clustering coefficient of FIn 
#~ print GetTriads(FIn) 
#~ print GetClustCf(FIn)
#~ print("succcess")
