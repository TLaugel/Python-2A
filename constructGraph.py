 #-*- coding: utf-8 -*-
import functools
import os
import snap
import linecache
import re
from parser import *
path = os.getcwd()

path = functools.reduce(add,path.split('/')[:-1])
name = "amazon-meta.txt"
name = '/'+name
f = open(path+name, 'r')

print 'start'
CustomerFile = open("UniqueCustomerProd.txt")
dicCustom = {}
id = 0
for line in CustomerFile :
	line = re.sub(repl,'',line)
	if not(line in dicCustom) :
		dicCustom[line] = id
		id += 1
CustomerFile.close()
print 'I know my customer !'

		
class MyProductCustom():
	def __init__(self,file) :
		currentProd = MyProduct(file)
		self.ASIN = currentProd.ASIN
		self.Id = currentProd.Id
		self.customers = []
		for review in currentProd.reviews.reviews :
			self.customers.append(review.customer)
		self.similarProd = []
		for sim in currentProd.similars.similar :
			self.similarProd.append(sim)
	def AddEdgeProduct(self,graph,idProd) : #add the edges corresponding to similar products
		for simProd in self.similarProd :
			if simProd in idProd:
				graph.AddEdge(self.Id,idProd[simProd].Id)
	def AddEdgeCustomer(self,graph,idCustom) :
		for cust in self.customers:
			if cust in idCustom:
				graph.AddEdge(2*self.Id,2*idCustom[cust]+1)
	def saveJson(self):
		print self.ASIN
		

if __name__  == '__main__' :
	
	for i in range(2) : #remove the first useless lines
		f.readline()
	a = []
	i = 0			
	id = 0
	GraphSim = snap.TNEANet.New()
	GraphBipartiteProdPeople = snap.TNEANet.New() #odd number : buyer, even : product
	IdProd= {}
	while 1 :
		try :
			a = MyProductCustom(f)
			ASIN = a.ASIN
			IdProd[ASIN] = a
		except :
			break
	
	#adding the node
	for product in IdProd :
		GraphSim.AddNode(IdProd[product].Id)
		GraphBipartiteProdPeople.AddNode(2*IdProd[product].Id)
	for people in dicCustom:
		GraphBipartiteProdPeople.AddNode(2*dicCustom[people]+1)
	for el in IdProd :
		IdProd[el].AddEdgeProduct(GraphSim,IdProd)
		IdProd[el].AddEdgeCustomer(GraphBipartiteProdPeople,dicCustom)
		
	print GraphSim.GetNodes()
	print GraphSim.GetEdges()
	FOut = snap.TFOut("GraphSimProduct.graph") #define by the similarity between products
	GraphSim.Save(FOut)
	FOut.Flush()
	
	FOut = snap.TFOut("GraphBipartite.graph") #define by the similarity between products
	GraphBipartiteProdPeople.Save(FOut)
	FOut.Flush()
