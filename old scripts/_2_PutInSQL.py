import numpy as np
import pandas
import time
import datetime
path = "../../"
#~ import pyximport; pyximport.install()


#~ python setup.py build_ext --inplace

#~ def mydateparser(str) :
	#~ print str
	#~ return time.strptime(str, "%Y-%m-%d") 
#~ cimport numpy as np
#~ import pandas as pd
#~ import datetime
#~ import numpy as np
#~ def convert_date_cython(np.ndarray date_vec, np.ndarray time_vec):
    #~ cdef int i
    #~ cdef int N = len(date_vec)
    #~ cdef out_ar = np.empty(N, dtype=np.object)
    #~ date = None
    #~ for i in range(N):
        #~ if date is None or date_vec[i] != date_vec[i - 1]:
            #~ dt_ar = map(int, date_vec[i].split("/"))
            #~ date = datetime.date(dt_ar[2], dt_ar[0], dt_ar[1])
        #~ time_ar = map(int, time_vec[i].split(".")[0].split(":"))
        #~ time = datetime.time(time_ar[0], time_ar[1], time_ar[2])
        #~ out_ar[i] = pd.Timestamp(datetime.datetime.combine(date, time))
    #~ return out_ar
    
nameIn = "ReviewsDatabase.txt"
if __name__ == "__main__":
	fileIn = open(path+nameIn,'r')
	fileIn.readline()
	i = 0
	n5 = 0
	for line in fileIn :
		i += 1
		if int(line.split('@')[4]) == 5 :
			n5 += 1
	print i
	print n5
	fileIn.close()
	#~ fileIn.close()
	#~ print nameVars[0]
	#~ print time.strptime("2001-12-31", "%Y-%m-%d")
	#~ DF = pandas.io.parsers.read_csv(path+nameIn,
								#~ sep=sepMain,
								#~ names = nameVars,
								#~ header=True,
								#parse_dates={'date': ['date']},
								#parse_dates= [2],
								#parse_dates= False,
								#index_col='date',
								#compression = 'gzip',
								#dtype = dtypes
								#date_parser = mydateparser
								#skip_blank_lines = True
								#~ )
	#~ print DF.shape
	#~ print DF[DF["ratingReview"]==5].shape
	