 #-*- coding: utf-8 -*-
import functools
import os
import snap
import linecache
import re
path = os.getcwd()


repl = '\s*'
def add(x,y): return x+'/'+y

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
def find_in_line(exp,line,found) :
	#~ print exp
	#~ print line[0]
	#~ print exp in line[0]
	if exp in line[0] and found:
		return line[0].split(exp),True
	else :
		return line,False
		
def extract_attrib(attribute,file,found,line) :
	if found :
		line = file.readline()
		#~ print line
	if attribute in line:
		return line.split(attribute)[-1],True,line
	else :
		return [],False,line
		
class Review : #one single review
	def __init__(self,line) :
		line = [line]
		found = True
		line,found = find_in_line('helpful:',line,found )
		#~ self.helpful = int(line[-1])
		helpful = int(line[-1])
		
		line,found = find_in_line('votes:',line,found )
		#~ self.votes = int(line[-1])
		votes = int(line[-1])
		
		line,found = find_in_line('rating:',line,found )
		#~ self.rating = int(line[-1])
		rating = int(line[-1])
		
		line,found = find_in_line('cutomer:',line,found )
		self.customer = line[-1]
		#~ self.date = line[0].replace(' ','')
		date = line[0].replace(' ','')
class Reviews : #all reviews
	def __init__ (self,file,bool):
		line = [re.sub(repl,'',file.readline())]
		found = bool
		line,found = find_in_line('avgrating:',line,found)
		if found :
			#~ self.avgRating = float(line[-1])
			avgRating = float(line[-1])
		else :
			#~ self.avgRating = -1.0
			avgRating = -1.0
		line,found  = find_in_line('downloaded:',line,found )
		if found: 
			#~ self.downloaded = int(line[-1])
			downloaded = int(line[-1])
		else :
			#~ self.downloaded = 0
			downloaded = 0
		line,found  = find_in_line('total:',line,found )
		if found :
			#~ self.nb = int(line[-1])
			nb = int(line[-1])
		else :
			#~ self.nb = 0
			nb = 0
		self.reviews = []
		#~ for i in range(self.downloaded) :
		for i in range(downloaded) :
			line = re.sub(repl,'',file.readline())
			#~ self.reviews.append(Review(line))
			self.reviews.append(Review(line).customer)
			
class Categorie : #one single categorie
	def __init__(self,line):
		#~ print line
		test = line.split('[')
		if len(test) == 2 :
			self.name = test[0]
		else :
			self.name = functools.reduce(self.remerge,test[:-1])
			#~ print line.split('[')[1].replace(']','')
		self.number = int(test[-1].replace(']',''))
	def remerge(self,str1,str2) :
		return str1+'['+str2
class CategorieTree : #one single categorie tree
	def __init__(self,line):
		#~ print line
		cats  = line.split('|')[1:]
		self.categories = []
		for cat in cats :
			self.categories.append(Categorie(cat))		
class CategoriesTrees : #all the categorie trees
	def __init__(self,file,bool):
		if bool :
			line = re.sub(repl,'',file.readline())
			nb = int(line.split(':')[-1])
			self.categoriesTree = []
			for i in range(nb):
				line  =re.sub(repl,'',file.readline())
				self.categoriesTree.append(CategorieTree(line))
		else :
			nb = 0
			self.categoriesTree = []
class Similars : #all similar product
	def __init__(self,file,found):
		if found :
			line = file.readline()
			splitted = line.replace('\n','').replace('\r','').split('similar:')[-1].split('  ')
			#~ print splitted
			self.number = int(splitted[0])
			self.similar = [] #list of ASIN
			for i in range(self.number):
				self.similar.append(re.sub(repl,'',splitted[i+1]))
		else :
			self.number = 0
			self.similar = []
		
class MyProduct:
	def __init__(self,file) :
		line = re.sub(repl,'',file.readline())
		if line == '' :
			line = re.sub(repl,'',file.readline())
		self.Id  = int(line.split(':')[-1])
		if self.Id% 10000 == 0 :
			print self.Id
		#~ print self.Id
		self.ASIN = re.sub(repl,'',file.readline()).split(':')[-1]
		#~ print self.ASIN
		found = True
		#~ self.title,found,line = extract_attrib('title:',file,found,"")
		title,found,line = extract_attrib('title:',file,found,"")
		#~ self.group,found,line  = extract_attrib('group:',file,found,line)
		group,found,line  = extract_attrib('group:',file,found,line)
		#~ self.salesrank,found,line  = extract_attrib('salesrank:',file,found,line)
		salesrank,found,line  = extract_attrib('salesrank:',file,found,line)
		self.similars = Similars(file,found)
		#~ similars = Similars(file,found)
		#~ self.categories = CategoriesTrees(file,found)
		categories = CategoriesTrees(file,found)
		self.reviews = Reviews(file,found)
		#~ reviews = Reviews(file,found)
		#~ self.customUnique = set(map(lambda x : x.customer,reviews.reviews))))
		#~ for el in set(map(lambda x : x.customer,reviews.reviews)) :
			#~ print el.replace('\r','').replace('\n','').replace(' ','').replace('\t','')
		
	def AddEdgeProduct(self,graph,idProd) : #add the edges corresponding to similar products
		#~ print self.Id
		for simProd in self.similars.similar :
			if simProd in idProd:
				graph.AddEdge(self.Id,idProd[simProd].Id)
				#~ print "I have one !"
			#~ else :
				#~ print simProd
	def AddEdgeCustomer(self,graph,idCustom) :
		for review in self.reviews.reviews:
			cust = review
			#~ cust = review.customer 
			if cust in idCustom:
				graph.AddEdge(2*self.Id,2*idCustom[cust]+1)
	def saveJson(self):
		print self.ASIN
		#~ print"["
		#~ res =  "{"+str(self.ASIN)+": ["
		#~ if len(self.similars.similar) > 0 :
			#~ for el in self.similars.similar :
				#~ res += el+","
			#~ res = res[:-1]
		#~ res+="]}"
		#~ print res
		#~ print"]"
		

if __name__  == '__main__' :
	
	for i in range(2) : #remove the first useless lines
		f.readline()
	a = []
	i = 0
	#~ while(1) :
		#~ try :
			#~ a = MyNode(f)
			#~ i+=1
			#~ #if len(a.categories.categoriesTree) > 0 :
				#~ #if(a.categories.categoriesTree[0].categories) > 0 :
					#~ #print a.categories.categoriesTree[0].categories[0].number
		#~ except :
			#~ break
	#~ f.close()
	#~ print i
			
	id = 0
	GraphSim = snap.TNEANet.New()
	GraphBipartiteProdPeople = snap.TNEANet.New() #odd number : buyer, even : product
	IdProd= {}
	while 1 :
		try :
			 a = MyProduct(f)
			 ASIN = a.ASIN
			 IdProd[ASIN] = a
			 #~ a.saveJson()
		except :
			break
	#~ for el in ["1551804247","0762722266","0440235014","1558702067","0440503744"] :
		#~ print el in IdProd
	#~ print len(IdProd)
	
	#~ #adding the node
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
	GraphSim.save(FOut)
	FOut.flush()
	
	FOut = snap.TFOut("GraphBipartite.graph") #define by the similarity between products
	GraphBipartiteProdPeople.save(FOut)
	FOut.flush()
	
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
				
	#~ counter = 0
	#~ ff = open(path+name, 'r')
	#~ out = open(path+"/first100", 'w')
	#~ for line in ff:
		#~ out.write(line)
		#~ if(counter > 5000) :
			#~ break
		#~ counter += 1
	#~ ff.close()
	#~ out.close()
	#~ print G1.GetNodes()
	#~ print G1.GetEdges()



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
