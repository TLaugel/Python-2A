#-*- coding: utf-8 -*-
AsinFile = open("ASINSimilarJSON.json")
AsinProd = []
for line in AsinFile :
	AsinProd.append(line.replace('\n','').replace('\r','').replace(' ','').replace('\t',''))
AsinFile.close()
Similar= open("ASINSimilars.txt")
AsinSim = []
for line in Similar :
	AsinSim.append(line.replace('\n','').replace('\r','').replace(' ','').replace('\t',''))

AsinProd = set(AsinProd)
AsinSim = set(AsinSim)
print "AsinProd contient",len(AsinProd)
print "AsinSim contient", len(AsinSim)
print len(AsinSim & AsinProd)
