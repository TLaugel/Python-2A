from parser import MyProduct
import gzip
from _1_constructDataBase import path,nameIn
primaryCat = ['3375251', '283155', '5174', '3489201', '229220', '139452', '1064952', '265523', '171280', '172282', '229534', '540744', '468642', '700060']
dic = {}
class MyProductSave() :
	def __init__(self,fileIn,dic) :
		currentProd = MyProduct(fileIn)
		for cat in currentProd.categories.categoriesTree :
			currCat = cat.categories[0]
			if not (currCat.number) in dic :
				dic[currCat.number] = currCat.name
		
if __name__ == "__main__":
	fileIn = gzip.open(path+nameIn, 'r')
	for i in range(2) : #remove the first useless lines
		fileIn.readline()
	i = 0
	while 1 :
		try :
			i += 1
			a = MyProductSave(fileIn,dic)
		except :
			break
		if len(dic) == len(primaryCat) :
			break
	fileIn.close()
	print dic
	
	#{171280: '', 468642: '', 229220: '', 1055398: '', 540744: '', 700060: '', 283155: 'Books', 3489201: 'Sportsrus.com', 265523: '', 3375251: 'Sports&Outdoor', 5174: 'Music', 172282: '', 139452: '', 229534: ''}
