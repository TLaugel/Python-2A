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
def find_in_line(exp,line,found) :
	if exp in line[0] and found:
		return line[0].split(exp),True
	else :
		return line,False
		
def extract_attrib(attribute,file,found,line) :
	if found :
		line = file.readline()
	if attribute in line:
		return line.split('group:')[-1],True,line
	else :
		return [],False,line

class Reviews : #all reviews
	def __init__ (self,file):
		line = [file.readline().replace('\n','').replace('\r','')]
		found = True
		line,found = find_in_line('avg rating:',line,found)
		self.avgRating = float(line[-1])
		line,found  = find_in_line('downloaded:',line,found )
		self.dowloaded = int(line[-1])
		line,found  = find_in_line('total:',line,found )
		self.nb = int(line[-1])
		self.reviews = []
		for i in range(self.dowloaded) :
			line = file.readline()
			self.reviews.append(Review(line))
class Review : #one single review
	def __init__(self,line) :
		line = [line]
		found = True
		line,found = find_in_line('helpful:',line,found )
		self.helpful = int(line[-1])
		
		line,found = find_in_line('votes:',line,found )
		self.votes = int(line[-1])
		
		line,found = find_in_line('rating:',line,found )
		self.rating = int(line[-1])
		
		line,found = find_in_line('cutomer:',line,found )
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
		
class MyNode 
	def __init__(self,file) :
		line = file.readline().replace('\r','').replace('\n','').replace(' ','')
		if line == '' :
			line = file.readline().replace('\r','').replace('\n','').replace(' ','')
		self.Id  = int(line.split(':')[-1])
		print self.Id
		self.ASIN = file.readline().split(':')[-1].replace('\r','').replace('\n','')
		#~ print self.ASIN
		found = True
		#~ print self.ASIN
		self.title,found,line = extract_attrib('title:',file,found,"")
		#~ if  'discontinued product' in self.title  :
			#~ return
		#~ else :
		#~ print self.title
		#~ print found
		self.group,found,line  = extract_attrib('group:',file,found,line)
		#~ print self.group
		self.salesrank,found,line  = extract_attrib('salesrank:',file,found,line)
		#~ print self.salesrank
		if found:
			self.similars = Similars(file.readline())
			#~ print self.similar.similar
			self.categories = Categories(file)
			self.reviews = Reviews(file)
			#~ file.readline()
		#~ for re in self.reviews.reviews :
			#~ print re.date
for i in range(1) : #remove the first useless lines
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