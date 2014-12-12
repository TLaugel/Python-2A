import functools
import os
import linecache
import re
from constructDataBase import sepMain,sep2,sep3
path = os.getcwd()

path = '/'.join(path.split('/')[:-1])+'/'
#~ First = set()
#~ Second = set()
#~ Third = set()
#~ Fourth = set()
#~ Fifth = set()
#~ Sixth = set()
#~ Seventh = set()
#~ Eighth = set()
#~ Nineth = set()
#~ dicSec = {0:First,1:Second,2:Third,3:Fourth,4:Fifth,5:Sixth,6:Seventh,7:Eighth,8:Nineth}
nameOut = "sortedDataBase.txt"
primaryCat = ['3375251', '283155', '5174', '3489201', '229220', '139452', '1064952', '265523', '171280', '172282', '229534', '540744', '468642', '700060']
dicPrimaryCatSeen_Ref = {}
if __name__ == "__main__" :
	import subprocess
	command = "sort -t '@' %PATH%unorderedDatabase.txt -o %PATH%sortedDataBase.txt".replace("%PATH%",path)
	print "execution of "+command
	os.system(command)
	print "now we can work properly"
	fIn = open(path+name,'r')
	fOut = open(path+'sortedDataBaseWithCust.txt','w')
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
	
	
	
	
	