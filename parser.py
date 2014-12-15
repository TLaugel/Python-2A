 #-*- coding: utf-8 -*-
import functools
import os
import snap
import linecache
import re
path = os.getcwd()

repl = '\s*'
def add(x,y): return x+'/'+y

#~ path = functools.reduce(add,path.split('/')[:-1])
#~ name = "amazon-meta.txt"
#~ name = '/'+name
#~ f = open(path+name, 'r')
def find_in_line(exp,line,found) :
	if exp in line[0] and found:
		return line[0].split(exp),True
	else :
		return line,False
		
def extract_attrib(attribute,file,found,line) :
	if found :
		line =  re.sub(repl,'',file.readline())
	if attribute in line:
		return line.split(attribute)[-1],True,line
	else :
		return [],False,line
		

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
		
class Reviews : #all reviews
	def __init__ (self,file,bool):
		line = [re.sub(repl,'',file.readline())]
		found = bool
		line,found = find_in_line('avgrating:',line,found)
		if found :
			self.avgRating = float(line[-1])
		else :
			self.avgRating = -1.0
		line,found  = find_in_line('downloaded:',line,found )
		if found: 
			self.downloaded = int(line[-1])
		else :
			self.downloaded = 0
		line,found  = find_in_line('total:',line,found )
		if found :
			self.nb = int(line[-1])
		else :
			self.nb = 0
		self.reviews = []
		for i in range(self.downloaded) :
			line = re.sub(repl,'',file.readline())
			self.reviews.append(Review(line))
			
class Categorie : #one single categorie
	def __init__(self,line):
		test = line.split('[')
		if len(test) == 2 :
			self.name = test[0]
		else :
			self.name = functools.reduce(self.remerge,test[:-1])
		self.number = int(test[-1].replace(']',''))
	def remerge(self,str1,str2) :
		return str1+'['+str2
		
class CategorieTree : #one single categorie tree
	def __init__(self,line):
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
			line = file.readline() #it is normal that there is no re.sub(repl,'',file.readline())
			splitted = line.replace('\n','').replace('\r','').split('similar:')[-1].split('  ')
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
		self.ASIN = re.sub(repl,'',file.readline()).split(':')[-1]
		found = True
		self.title,found,line = extract_attrib('title:',file,found,"")
		self.group,found,line  = extract_attrib('group:',file,found,line)
		self.salesrank,found,line  = extract_attrib('salesrank:',file,found,line)
		self.similars = Similars(file,found)
		self.categories = CategoriesTrees(file,found)
		self.reviews = Reviews(file,found)