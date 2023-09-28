# import sys
# sys.path.append('../scripts')

import os
import json

import numpy as np
import matplotlib.pyplot as plt

from HYDRO_Stats import TrendDetector

def genTrendPlotJson(outputJsonPath='./hydroJson/TrendPlot.json', returnDict=False):
    """
    Summary:
    ---
    Generate a json file of drawing parameters for easy adjustment
    """
    PARAMETERS = {
        "obs_marker"        : "o",
        "obs_marker_size"   : 1,
        "obs_line_width"    : 0.5,
        "obs_line_style"    : "-",
        "obs_line_color"    : "k",
        "obs_label"         : "Observed",
        
        "fit_marker"        : "^",
        "fit_marker_size"   : 1,
        "fit_line_width"    : 0.5,
        "fit_line_style"    : "--",
        "fit_line_color"    : "r",
        "fit_label"         : "Fitted",
        
        "x_label"           : "X Label",
        "y_label"           : "Y Label",
        
        "x_lim"             : [],
        "y_lim"             : [],
        "expand_top"        : 0.2,
        "expand_bottom"     : 0.1,
        
        "x_tick"            : [],
        "y_tick"            : [],
        
        
        "has_legend"        : True,
        "legend_loc"        : 1,
        "legend_fontsize"   : 8,

        "has_fit_text"      : True,
        "text_string"       : "k = {:.2f}, p = {:.5f}",
    }
    
    if not os.path.exists(os.path.dirname(outputJsonPath)):
        os.mkdir(os.path.dirname(outputJsonPath))
        
    with open(outputJsonPath, "w", encoding='utf-8') as f:
        json.dump(PARAMETERS, f, indent=2)  
    
    print("Json file of parameters has written to [{}]".format(outputJsonPath))
    
    if returnDict:
        return PARAMETERS


class TrendPlot:
    """
    该类必须需要传入一个ax对象
    """
    def __init__(self, ax, jsonPath='./hydroJson/TrendPlot.json'):
        assert os.path.isfile(jsonPath), "Json file doesn't exist! "
        self.jsonPath = jsonPath
        with open(jsonPath) as f:
            self.paraDict = json.load(f)
        self.ax = ax
            
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
        
        # original line plot
        marker  = PARAS['obs_marker']
        ms      = PARAS['obs_marker_size']
        ls      = PARAS['obs_line_style']
        lw      = PARAS['obs_line_width']
        color   = PARAS['obs_line_color']
        
        self.ax.plot(x, y, marker=marker, ms=ms, ls=ls, color=color, lw=lw, label=PARAS['obs_label'])

        
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

        # fit line plot
        self.ax.plot(x, fit_y, marker=marker, ms=ms, ls=ls, color=color, lw=lw, label=PARAS['fit_label'])
        
        if PARAS['x_lim']:
            self.ax.set_xlim(PARAS['x_lim'])
        if PARAS['y_lim']:
            self.ax.set_ylim(PARAS['y_lim'])
        else:
            diff = np.nanmax(y) - np.nanmin(y)
            self.ax.set_ylim([np.nanmin(y)-diff*PARAS['expand_bottom'], np.nanmax(y)+diff*PARAS['expand_top']])
        
        # set labels 
        if PARAS['x_label']:
            self.ax.set_xlabel(PARAS['x_label'])
        if PARAS['y_label']:
            self.ax.set_ylabel(PARAS['y_label'])
        
        
        # set legend
        if PARAS['has_legend']:
            self.ax.legend(loc=PARAS['legend_loc'], fontsize=PARAS['legend_fontsize'])
            
        # set ticks
        XTickParas = PARAS['x_tick']
        if len(XTickParas) == 3:
            self.ax.set_xticks(np.linspace(XTickParas[0], XTickParas[1], XTickParas[2]))
        elif len(XTickParas) >= 4:
            self.ax.set_xticks(XTickParas)
        elif len(XTickParas) == 0:
            pass
        else:
            print("Lenght of XTickParas is not valid!")
        
        YTickParas = PARAS['y_tick']
        if len(YTickParas) == 3:
            self.ax.set_yticks(np.linspace(YTickParas[0], YTickParas[1], YTickParas[2]))
        elif len(YTickParas) >= 4:
            self.ax.set_yticks(YTickParas)
        elif len(YTickParas) == 0:
            pass
        else:
            print("Lenght of YTickParas is not valid!")
        
            
        # fit text
        if PARAS['has_fit_text']:
            text_string = PARAS['text_string']
            text_string = text_string.format(k, fitDict['pValue'])
            self.ax.text(0.02, 0.95, text_string, transform=self.ax.transAxes, verticalalignment='center', horizontalalignment='left', fontsize=8)


def quickTrendPlot(x, y=None):
    """
    快速画出x,y的折线图，并给出拟合直线的图。其中x,y均为一维数据，若y为空，则默认为0,1,2,3...
    """
    if y == None:
        y = np.arange(0, len(x))
        a = x
        x = y
        y = a
        del a
    assert len(x) == len(y), "Length of x and y must be equal!"
    
    fig = plt.figure(figsize=(8, 4), dpi=300)
    ax = fig.add_subplot(111)
    genTrendPlotJson('./hydroJson/quickTrendPlot.json', returnDict=False)
    tp = TrendPlot(ax, './hydroJson/quickTrendPlot.json')
    tp.plot(x, y)
    