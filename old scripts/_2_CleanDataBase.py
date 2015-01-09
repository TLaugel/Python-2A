import functools
import os
import linecache
import re
import gzip
from _1_constructDataBase import sepMain,sep2,sep3,nameOut,path

nameIn = nameOut
nameAux = "sortedDataBase.txt"
nameOut = "sortedDataBaseWithCust.txt.gz"

primaryCat = ['3375251', '283155', '5174', '3489201', '229220', '139452', '1064952', '265523', '171280', '172282', '229534', '540744', '468642', '700060']

283155 = Books
5174 = Music

dicPrimaryCatSeen_Ref = {}
if __name__ == "__main__" :
	import subprocess
	command = "sort -t '%SEPCOL%' %PATHIn% -o %PATHAux%".replace("%PATHIn%",path+nameIn).replace("%PATHAux%",path+nameAux).replace("%SEPCOL%",sepMain)
	print "execution of "+command
	os.system(command)
	print "now we can work properly"
	fIn = open(path+nameAux,'r')
	fOut = gzip.open(path+nameOut,'w')
	for el in primaryCat :
		dicPrimaryCatSeen_Ref[el] = 0
	li_prod_customer = []
	currentUser = ''
	for line in fIn :
		splitted = line.replace('\r\n','').split(sepMain)
		user = splitted[0]
		if user == currentUser :
			li_prod_customer.append(splitted)
		else :
			for prod in li_prod_customer :
				cat = prod[10].split(sep2)
				primCat = map(lambda x : x.split(sep3)[0],cat)
				for el in primCat :
					dicPrimaryCatSeen[el] += 1
					
			for prod in li_prod_customer :
				newli = prod
				newli += map(lambda x : str(dicPrimaryCatSeen[x]),primaryCat)
				newli = sepMain.join(newli)+'\r\n'
				fOut.write(newli)
			dicPrimaryCatSeen = dicPrimaryCatSeen_Ref.copy()
			li_prod_customer = [splitted]
			currentUser = user

	fIn.close()
	fOut.close()
	
	
	
	
	
