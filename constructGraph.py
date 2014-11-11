 #-*- coding: utf-8 -*-
import functools
import os
from snap import *
path = os.getcwd()
def add(x,y): return x+'/'+y
path = functools.reduce(add,path.split('/')[:-1])
name = "amazon-meta.txt"
name = '/'+name
f = open(path+name, 'r')
#~ str = "similar: 5 1559360968 1559361247 1559360828 1559361018 0743214552"
#~ print(map(int,str.split(':')[-1].split()[1:]))

id = 0
G1 = TNEANet.New()
dic = {}
intId = 1
idNode = intId
for line in f:
	line = line.replace('\r','').replace('\n','')
	if line[0:4] == 'ASIN' :
		id = line.split(':')[-1]
		if not(id in dic):
			dic[id] = intId
			G1.AddNode(intId)
			intId += 1
		idNode = dic[id]
	if(line[0:9] ==  "  similar"):
		try :
			def addEdge(x):
				if not(x in dic):
					global intId
					dic[x] = intId
					G1.AddNode(intId)
					intId +=  1
				G1.AddEdge(idNode,dic[x] )
			li = line.split(':')[-1].split()[1:]
			map(addEdge,line.split(':')[-1].split()[1:])			
		except :
			pass
		
print G1.GetNodes()
print G1.GetEdges()

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
