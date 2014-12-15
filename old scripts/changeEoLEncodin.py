FIn = open('../FinalSimpleDB.txt','r')
Fout = open('../Final.csv','w')
for line in FIn :
	line = line.replace('\r\n','\n')
	Fout.write(line)
FIn.close()
Fout.close()