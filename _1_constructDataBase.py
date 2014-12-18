import functools
import os
import linecache
import re
import gzip
#~ f = gzip.open('file.txt.gz', 'rb')
#~ file_content = f.read()
#~ f.close()
from parser import MyProduct
path = os.getcwd()

path = '/'.join(path.split('/')[:-1])+'/'
nameIn = "amazon-meta.txt.gz"
#~ nameOut = "unorderedDatabase.txt"
nameOut = "ReviewsDatabase.txt"
nameVars = ["idCus","idProd","date","prodCat","rating"]
sepMain  = '@'
sep2 = '^'
sep3 = '$'

#~ dicProd = {} #key : ASIN, value : first categorie
#~ class ProductId () :
	#~ def __init__(self,fileIn):
		#~ currentProd = MyProduct(fileIn)
		#~ if ! currentProd.ASIN in dicProd :
			#~ dicProd[currentProd.ASIN] = 
		
class MyProductSave():
	def __init__(self,fileIn,fileOut) :
		currentProd = MyProduct(fileIn)
		self.writeReview(currentProd,fileOut)
		
	def writeReview(self,currentProd,fileOut) :
		ASIN = currentProd.ASIN
		#~ similarProduct = sep2.join(currentProd.similars.similar)
		#~ avgRating = currentProd.reviews.avgRating
		#~ nbReviews = str(currentProd.reviews.nb)
		
		#~ nbHelpFull = 0
		#~ currentSum = 0
		#~ for rev in currentProd.reviews.reviews :
			#~ currentSum += rev.helpful * rev.rating
			#~ nbHelpFull += rev.helpful
		#~ avgRatingHelpful = 0
		#~ if nbHelpFull > 0 :
			#~ avgRatingHelpful = currentSum/nbHelpFull
		#~ salesRank = currentProd.salesrank
		#~ categories = []
		#~ for cat in currentProd.categories.categoriesTree :
			#~ categories.append( sep3.join(map(lambda x : str(x.number),cat.categories)))
		#~ categories =  sep2.join(categories)
		#~ res = ''
		#~ for rev in currentProd.reviews.reviews :
			#~ res = rev.customer+sepMain
			#~ res += rev.date+sepMain
			#~ res += str(rev.rating)+sepMain
			#~ res += ASIN+sepMain
			#~ res += str(avgRating)+sepMain
			#~ res += nbReviews+sepMain
			#~ res += str(avgRatingHelpful)+sepMain
			#~ res += str(nbHelpFull)+sepMain
			#~ res += salesRank+sepMain
			#~ res += similarProduct+sepMain
			#~ res += categories
			#~ fileOut.write(res+'\r\n')
		for rev in currentProd.reviews.reviews :
			res = rev.customer+sepMain
			res += ASIN+sepMain
			res += rev.date+sepMain
			res += str(currentProd.categories.categoriesTree[0].categories[0].number)+sepMain
			res += str(rev.rating)
			#~ print res
			fileOut.write(res+'\n')
		
		
if __name__ == "__main__" :
	fileIn = gzip.open(path+nameIn, 'r')
	fileOut = open(path+nameOut,'w')
	for i in range(2) : #remove the first useless lines
		fileIn.readline()
	i = 0
	res = sepMain.join(nameVars) 
	fileOut.write(res+'\n')
	while 1 :
		try :
			i += 1
			a = MyProductSave(fileIn,fileOut)
		except :
			break

	fileIn.close()
	fileOut.close()