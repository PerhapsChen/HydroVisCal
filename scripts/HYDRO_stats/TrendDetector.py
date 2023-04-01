import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from scipy.stats.mstats import theilslopes
from scipy.stats import kendalltau
from tqdm.notebook import tqdm

class TrendDetector:    
    def __init__(self, method='linear') -> None:
        """support both 1D and 3D, linear and sen method.
        -- Modified from my advisor MAO Ganquan
        
        Args:
            method (str, optional): 'linear' or 'sen'. Defaults to 'linear'.
        """
        assert method in ['linear', 'sen']
        self.method = method

    def trendLinear1D(self, arr):
        if type(arr) != np.ndarray:
            arr = np.array(arr)
        assert len(arr.shape)==1
        if np.all(arr==0) or np.sum(np.isnan(arr))+np.sum(np.isinf(arr))>=(arr.shape[0]/2): 
        # the number of nan and inf should less than half of array lenth
            return {    'changeValue': np.nan,
                        'mean'       : np.nan,
                        'changeRatio': np.nan,
                        'pValue'     : np.nan,
                        'slope'      : np.nan,
                        'intercept'  : np.nan   }

                
        
        dataX= np.arange(arr.shape[0])
        dataY = arr.copy()
        isFinite = np.isfinite(arr)
        dataX = dataX[isFinite]
        dataY = dataY[isFinite]
        isNotNan = ~np.isnan(arr)
        dataX = dataX[isNotNan]
        dataY = dataY[isNotNan]
        
        if self.method == 'linear':

            fit = np.polyfit(dataX, dataY, 1)
            model = np.poly1d(fit)
            df = pd.DataFrame(columns=['y', 'x'])
            df['x'] = dataX
            df['y'] = dataY
            results = smf.ols(formula='y ~ model(x)', data=df).fit()
            pValue = results.f_pvalue
            slope = fit[0]
            intercept = fit[1]
        elif self.method=='sen':
            _, pValue = kendalltau(dataX, dataY)
            slope, intercept, _, _ = theilslopes(dataX, dataY)
        return {'changeValue': slope*len(arr),
                'mean'       : np.nanmean(dataY),
                'changeRatio': (slope * len(arr)) / np.nanmean(dataY) * 100,
                'pValue'     : pValue,
                'slope'      : slope,
                'intercept'  : intercept}
        
    def trendLinear3D(self, arr):
        """
        Args:
            arr (_type_): Please guarantee time-coord is the zero-th axis
        """
        if type(arr) != np.ndarray:
            arr = np.array(arr)
        assert len(arr.shape)==3
        
        changeValue2D   = np.full_like(arr[0], np.nan, dtype=np.float32)
        mean2D          = np.full_like(arr[0], np.nan, dtype=np.float32)
        changeRatio2D   = np.full_like(arr[0], np.nan, dtype=np.float32)
        pValue2D        = np.full_like(arr[0], np.nan, dtype=np.float32)
        slope2D         = np.full_like(arr[0], np.nan, dtype=np.float32)
        intercept2D     = np.full_like(arr[0], np.nan, dtype=np.float32)
        
        NTime = arr.shape[0]
        NLat = arr.shape[1]
        NLon = arr.shape[2]
        for i in tqdm(range(NLat)):
            for j in range(NLon):
                arr1D = arr[:,i,j]
                resDict = self.trendLinear1D(arr1D)
                changeValue2D[i,j]  = resDict['changeValue']
                mean2D[i,j]         = resDict['mean']
                changeRatio2D[i,j]  = resDict['changeRatio']
                pValue2D[i,j]       = resDict['pValue']
                slope2D[i,j]        = resDict['slope']
                intercept2D[i,j]    = resDict['intercept']
                
        return {'changeValue': changeValue2D,
                'mean'       : mean2D,
                'changeRatio': changeRatio2D,
                'pValue'     : pValue2D,
                'slope'      : slope2D,
                'intercept'  : intercept2D}
                