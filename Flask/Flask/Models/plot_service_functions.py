
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import path
import io


def plot_to_img(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()). decode('utf8')
    return pngImageB64String

def GetNormalDataSet():
    df = pd.read_csv(path.join(path.dirname(__file__), "..\\static\\Data\\dataSet1.csv"))
    df = df.drop(['District', 'Age group', 'Gender', 'Education', 'Disability', 'Jobseekers', 'Hh', 'Non academic unemployment', 'Newcomers', 'Newcomers that got fired', 'Academic unemployment'], 1)
    df.rename(columns={ df.columns[4]: "c" }, inplace = True)
    df.rename(columns={ df.columns[3]: "a" }, inplace = True)
    df.rename(columns={ df.columns[2]: "b" }, inplace = True)
    df = df.drop(['a', 'b', 'c'], 1)
    df['My new column'] = 'default value'
    df = df.set_index(['Religion', 'Month'])
    df = df.sort_values(by='Religion')
    df = df.groupby(['Religion', 'Month']).count()
    df = df.loc[['אחר', 'דרוזים', 'מוסלמים', 'נוצרים', 'יהודים']]
    jews = [9716, 10004, 10134, 9899, 10137, 10256, 10493, 10327, 10233, 9963]
    christians = [1469, 1573, 1674, 1535, 1560, 1549, 1586, 1525, 1542, 1527]
    muslims = [5607, 5780, 6099, 5911, 5924, 5919, 6093, 5981, 6000, 5845]
    drushim = [1050, 1110, 1134, 1102, 1116, 1094, 1107, 1037, 1050, 1064]
    other = [3250, 3488, 3542, 3423, 3505, 3551, 3617, 3483, 3579, 3469]
    index = ['2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06', '2019-07', '2019-08', '2019-09', '2019-10']
    df = pd.DataFrame({'jews': jews, 'christians' : christians, 'muslims' : muslims, 'drushim' : drushim, 'other' : other}, index=index)
    return df