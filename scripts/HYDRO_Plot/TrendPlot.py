import sys
sys.path.append('../scripts')

import os
import json

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from HYDRO_Stats import TrendDetector

def genTrendPlotJson(outputJsonPath='./hydroJson/TrendPlot.json', returnDict=False):
    """
    Summary:
    ---
    Generate a json file of drawing parameters for easy adjustment
    """
    PARAMETERS = {
        "figsize"           : [8,4],
        "dpi"               : 200,
        
        "obs_marker"        : "o",
        "obs_marker_size"   : 1,
        "obs_line_width"    : 0.5,
        "obs_line_style"    : "-",
        "obs_line_color"    : "k",
        
        "fit_marker"        : "^",
        "fit_marker_size"   : 1,
        "fit_line_width"    : 0.5,
        "fit_line_style"    : "--",
        "fit_line_color"    : "r",
    }
    
    if not os.path.exists(os.path.dirname(outputJsonPath)):
        os.mkdir(os.path.dirname(outputJsonPath))
        
    with open(outputJsonPath, "w", encoding='utf-8') as f:
        json.dump(PARAMETERS, f, indent=2)  
    
    print("Json file of parameters has written to [{}]".format(outputJsonPath))
    
    if returnDict:
        return PARAMETERS


class TrendPlot:
    def __init__(self, jsonPath='./hydroJson/TrendPlot.json'):
        assert os.path.isfile(jsonPath), "Json file doesn't exist! "
        self.jsonPath = jsonPath
        with open(jsonPath) as f:
            self.paraDict = json.load(f)
            
    def reloadJson(self):
        with open(self.jsonPath) as f:
            self.paraDict = json.load(f)  
            
    def genDefaultJson(self):
        """
        go back to default json
        """
        genTrendPlotJson(self.jsonPath)
        
    def saveCurrentJson(self, outputJsonPath='./hydroJson/currentFromTrendPlot.json'):
        if not os.path.exists(os.path.dirname(outputJsonPath)):
            os.mkdir(os.path.dirname(outputJsonPath))
            
        with open(outputJsonPath, "w", encoding='utf-8') as f:
            json.dump(self.paraDict, f, indent=2)  
        
        print("Current parameters has written to [{}]".format(outputJsonPath)) 
        
    def plot(self, x, y):
        """
        画出x,y的折线图，并给出拟合直线的图。其中x,y均为一维数据
        """
        self.reloadJson()
        PARAS = self.paraDict
        
        fig = plt.figure(figsize=PARAS['figsize'],dpi=PARAS['dpi'])
        ax = fig.add_subplot(1, 1, 1)
        # original line plot
        marker  = PARAS['obs_marker']
        ms      = PARAS['obs_marker_size']
        ls      = PARAS['obs_line_style']
        lw      = PARAS['obs_line_width']
        color   = PARAS['obs_line_color']
        
        ax.plot(x, y, marker=marker, ms=ms, ls=ls, color=color, lw=lw, label='x')

        
        # trend fit plot
        td = TrendDetector(method='sen')
        fitDict = td.trend1D(y)
        k = fitDict['slope']
        b = fitDict['intercept']
        fit_y  = [k*(xi-x[0])+b for xi in x]
        
        marker  = PARAS['fit_marker']
        ms      = PARAS['fit_marker_size']
        ls      = PARAS['fit_line_style']
        lw      = PARAS['fit_line_width']
        color   = PARAS['fit_line_color']

        ax.plot(x, fit_y, marker=marker, ms=ms, ls=ls, color=color, lw=lw, label='x')
        
        
        
        ax.legend(loc=1)