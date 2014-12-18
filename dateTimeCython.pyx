cimport numpy as np
import pandas as pd
import datetime
import numpy as np
def convert_date_cython(np.ndarray date_vec):
    cdef int i
    cdef int N = len(date_vec)
    cdef out_ar = np.empty(N, dtype=np.object)
    date = None
    for i in range(N):
        if date is None or date_vec[i] != date_vec[i - 1]:
            dt_ar = map(int, date_vec[i].split("-"))
            date = datetime.date(dt_ar[0], dt_ar[1], dt_ar[2])
        time = datetime.time(0,0,0)
        out_ar[i] = pd.Timestamp(datetime.datetime.combine(date, time))
    return out_ar
