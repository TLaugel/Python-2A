import numpy as np
import pandas
import time
import datetime
from _1_constructDataBase import sepMain,nameOut,path,nameVars
#~ import pyximport; pyximport.install()
from dateTimeCython import convert_date_cython
nameIn  = nameOut
nameAux = ""
dtypes = [str,str,str, str, str] 


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
    
if __name__ == "__main__":
	#~ fileIn = open(path+nameIn,'r')
	#~ fileIn.close()
	#~ print nameVars[0]
	#~ print time.strptime("2001-12-31", "%Y-%m-%d")
	DF = pandas.io.parsers.read_csv(path+nameIn,
								sep=sepMain,
								names = nameVars,
								header=True,
								#~ parse_dates={'date': ['date']},
								#~ parse_dates= [2],
								#~ parse_dates= False,
								#~ index_col='date',
								#~ compression = 'gzip',
								#~ dtype = dtypes
								#~ date_parser = mydateparser
								#~ skip_blank_lines = True
								)
	DF["date"] = convert_date_cython(DF["date"].values)
	print type(DF["date"][0])
	print DF["date"][0]
	print len(DF.loc[DF["date"] < pandas.Timestamp(datetime.datetime.combine(datetime.date(2001,12,31), datetime.time(0,0,0))) ]) 
	print DF.shape
	