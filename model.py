#-*- coding: utf-8 -*-
import pandas
import numpy as np
import sklearn
import sqlite3
import os
import csv

from GetFinalDB import finalSep
from constructUserIded import primaryCat
#~ df = pandas.read_csv('../FinalSimpleDB.txt',sep = ';')
#~ if not os.exist('../FinalSimpleDB.db3') :
con = sqlite3.connect('../FinalSimpleDB.db3')
names = """idCust text, idProd text,date numeric, ratingReview integer, avgRating real, wAvgRating real,  nbReview integer, 
			nbHelpful integer, salesrank integer, %othervariables%""".replace("%othervariables%",','.join(["catCust"+str(i)+" integer" for i in range(1,len(primaryCat)+1)]))
nbVariables = len(names.split(','))
command = """create table if not exists DbSql (%names%);""".replace("%names%",names)
print command
#~ con.execute(command)

#~ print "the data base is created"
#~ csvReader = csv.reader(open('../FinalSimpleDB.txt'), delimiter=';')
#~ print "Let's insert !"
#~ for row in csvReader:
	#~ print row
	#~ command = """insert into DbSql (%%names%%) values (%dots%)""".replace('%%names%%',names.replace('integer','').replace('numeric','').replace('real','').replace('text','')).replace('%dots%',','.join(['?' for i in range(1,nbVariables+1)]))
	#~ print command
	#~ con.execute(command, row)

#~ con.execute(command)
#~ con.execute(""".separator '%sep%'
			#~ .import \"../FinalSimpleDB.txt\" DbSql """.replace("%sep%",finalSep))
#~ command = """load data local infile  \"../FinalSimpleDB.txt\" into table DbSql fields terminated by \"%sep%\" lines terminated by \"\r\n\"; """.replace("%sep%",finalSep)

create table DbSql(idCust text, idProd text,date numeric, ratingReview integer, avgRating real, wAvgRating real,  nbReview integer, nbHelpful integer, salesrank integer, catCust1 integer,catCust2 integer,catCust3 integer,catCust4 integer,catCust5 integer,catCust6 integer,catCust7 integer,catCust8 integer,catCust9 integer,catCust10 integer,catCust11 integer,catCust12 integer,catCust13 integer,catCust14 integer);
