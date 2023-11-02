import numpy as np
import pandas as pd


def fill_values_in_Feb29(arr_old, start_time, end_time):
    '''
    给定一个不包含2月29日的数组，返回一个包含2月29日的数组
    缺失的值认为是2月28日和3月1日的平均数
    '''
    times = pd.date_range(start_time, end_time, freq='D')
    if len(arr_old.shape)==3:
        arr_new = np.zeros((len(times), arr_old.shape[1], arr_old.shape[2]))
    else:
        arr_new = np.zeros(len(times))
    startIndex = 0
    for i, t in enumerate(times):
        if t.month!=2 or t.day!=29:
            arr_new[i] = arr_old[startIndex]
            startIndex += 1
        else:
            arr_new[i] = (arr_old[startIndex]+arr_old[startIndex+1])/2
    return arr_new