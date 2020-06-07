
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import path
import io
import datetime


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
    df = df.sort_values(by='Religion')
    return df

def GetSelectedReligions():
    df_religions = pd.read_csv(path.join(path.dirname(__file__), "..\\static\\Data\\dataSet1.csv"))
   # s = df_religions.set_index('Religion')
    print(df_religions.columns)
    df1 = df_religions.groupby('Religion').sum()
    l = df1.index
    m = list(zip(l, l))
    return m