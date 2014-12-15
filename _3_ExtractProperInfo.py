import functools
import os
import linecache
import re
import gzip

from _1_constructDataBase import sepMain,sep2,sep3,path
from _2_CleanDataBase import nameOut
finalSep = ';'
nameIn = nameOut
nameOut = "FinalDB.txt"
eolEncoding = '\n'

if __name__ == "__main__" :
	fIn = gzip.open(path+nameIn,'r')
	fOut = open(path+nameOut,'w')
	print "dealing with the input"
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
		fOut.write(finalSep.join(res)+eolEncoding)
	fIn.close()
	fOut.close()
	command = "sqlite3 < myScriptToConvert.script "
	print "create the sqlite database"
	os.system(command)