#-*- coding: utf-8 -*-
AsinFile = open("UniqueCustomerProd.txt")
Customer = []
for line in AsinFile :
	Customer.append(line.replace('\n','').replace('\r','').replace(' ','').replace('\t',''))
AsinFile.close()
print len(Customer)
print len(set(Customer))