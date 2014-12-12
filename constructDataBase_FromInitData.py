import functools
import os
import linecache
import re
from parser import *
path = os.getcwd()

path = functools.reduce(add,path.split('/')[:-1])+'/'
name = "amazon-meta.txt"

sepMain  = '@'
sep2 = '^'
sep3 = '$'

class MyProductSave():
	def __init__(self,fileIn,fileOut) :
		currentProd = MyProduct(fileIn)
		self.writeReview(currentProd,fileOut)
		
	def writeReview(self,currentProd,fileOut) :
		ASIN = currentProd.ASIN
		similarProduct = sep2.join(currentProd.similars.similar)
		avgRating = currentProd.reviews.avgRating
		nbReviews = str(currentProd.reviews.nb)
		
		nbHelpFull = 0
		currentSum = 0
		for rev in currentProd.reviews.reviews :
			currentSum += rev.helpful * rev.rating
			nbHelpFull += rev.helpful
		avgRatingHelpful = 0
		if nbHelpFull > 0 :
			avgRatingHelpful = currentSum/nbHelpFull
		salesRank = currentProd.salesrank
		categories = []
		for cat in currentProd.categories.categoriesTree :
			categories.append( sep3.join(map(lambda x : str(x.number),cat.categories)))
		categories =  sep2.join(categories)
		res = ''
		for rev in currentProd.reviews.reviews :
			res = rev.customer+sepMain
			res += rev.date+sepMain
			res += str(rev.rating)+sepMain
			res += ASIN+sepMain
			res += str(avgRating)+sepMain
			res += nbReviews+sepMain
			res += str(avgRatingHelpful)+sepMain
			res += str(nbHelpFull)+sepMain
			res += salesRank+sepMain
			res += similarProduct+sepMain
			res += categories
			fileOut.write(res+'\r\n')
		
		
if __name__ == "__main__" :
	fileIn = open(path+name, 'r')
	fileOut = open(path+'unorderedDatabase.txt','w')
	for i in range(2) : #remove the first useless lines
		fileIn.readline()
	i = 0
	while 1 :
		try :
			i += 1
			a = MyProductSave(fileIn,fileOut)
		except :
			break
	#~ print i
	fileIn.close()
	fileOut.close()