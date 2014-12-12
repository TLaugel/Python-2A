import functools
import os
import linecache
import re
from constructDataBase_FromInitData import sepMain,sep2,sep3
from constructUserIded import nameOut
finalSep = ';'
path = os.getcwd()

path = '/'.join(path.split('/')[:-1])+'/'

nameIn = nameOut
nameOut = "FinalSimpleDB.txt"
if __name__ == "__main__" :
	fIn = open(path+nameIn,'r')
	fOut = open(path+nameOut,'w')
	for line in fIn :
		line = line.replace('\r\n','')
		li = line.split(sepMain)
		res = [li[0],li[3],li[1]] #customer,product,date
		#the output : the rating :
		res.append(li[2])
		#add product info
		res += [li[4],li[6],li[5],li[8],li[7]] #avgrating, weighted avg rating,nb review,  nb helpful,salesrank 
		#add customer info
		res += li[11:]
		fOut.write(finalSep.join(res)+'\r\n')
	fIn.close()
	fOut.close()