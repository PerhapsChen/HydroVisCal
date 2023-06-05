"""_summary_
[CLASS][FUNCTION]
"""

from PIL import Image
import numpy as np
from matplotlib.colors import ListedColormap
import pandas as pd

def interpolate(arr, pcs):
    # interp from [N, 4] to [1024, 4]
    N = arr.shape[0]
    R = arr[:, 0]
    G = arr[:, 1]
    B = arr[:, 2]
    inc = 1.0/pcs
    idxff = np.arange(inc/2, 1.0-inc/2+0.0001, inc)
    idx = [int(i*N) for i in idxff]
    R_x = np.full(R.shape, np.nan)
    R_x[idx] = R[idx]
    G_x = np.full(G.shape, np.nan)
    G_x[idx] = G[idx]
    B_x = np.full(B.shape, np.nan)
    B_x[idx] = B[idx]
    R_x = R_x[idx[0]:idx[-1]+1]
    G_x = G_x[idx[0]:idx[-1]+1]
    B_x = B_x[idx[0]:idx[-1]+1]
    df = pd.DataFrame()
    df['R'] = R_x
    df['G'] = G_x
    df['B'] = B_x
    df = df.interpolate(method='linear')
    df['A'] = [1.0]*df.shape[0]

    return df.values


class ColorBarFromFig:
    def __init__(self, path, piece=None, reverse=False, inputPcs=None):
        """
        将一张色带图片转换为colorbar对象，支持横向或竖向
        注意，如果是非连续色带，需要输入图片中有几种颜色
        （无奈之举，由于我们输入图片的质量参差不齐，自己判断可能会出现问题）
        设置piece参数为目标cmap分段的数量，-1默认为不分段即连续
        设置reverse可以将色带反转

        Args:
            path (_type_): 图片的路径
            piece (int, optional): 需要分多少段，-1为不分段. Defaults to -1.
            reverse (bool, optional): 是否需要倒置. Defaults to False.
            inputPcs (_type_, optional): 输入的图片有多少段，如果是连续就不输入. Defaults to None.
        """
        self.path = path
        self.piece = piece
        self.reverse = reverse
        self.inputPcs = inputPcs

        img = Image.open(path)
        arr = np.array(img)

        if arr.shape[0] < arr.shape[1]:
            ll = arr[arr.shape[0]//2, :, :]
        else:
            ll = arr[:, arr.shape[1]//2, :]
        if ll.shape[-1] == 3:
            ll = np.concatenate((ll, np.full((ll.shape[0], 1), 255)), axis=1)
        ll = ll/255.0
        if reverse:
            ll = ll[::-1, :]

        if inputPcs != None:
            ll = interpolate(ll, inputPcs)

        if piece == None or piece == -1:
            res = ll
        elif piece in np.arange(1, 30):
            #inc = ll.shape[0]//piece
            idx = [int(i) for i in np.linspace(0, ll.shape[0]-1, piece)]
            res = ll[idx, :]

        newcmp = ListedColormap(res, name='hydro')
        self.cmap = newcmp
        self.cmapArray = res

    def getColorBar(self):
        """
        获得matplotlib colorbar对象
        """
        return self.cmap

    def getColorBarArray(self):
        """
        获得matplotlib colorbar的原始数组
        """

        return self.cmapArray
