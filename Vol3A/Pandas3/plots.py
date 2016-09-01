# plots.py
import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file('../../matplotlibrc')

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


titanic = pd.read_csv('titanic.csv')
def heading():
    heading = titanic.head()
    # save heading as heading.pdf

def gend_surv():
    tab = titanic.groupby('sex')[['survived']].mean()
    # save tab as gend_surv.pdf

def gend_class():
    tab = titanic.groupby(['sex', 'class'])[['survived']].aggregate('mean').unstack()
    # save tab as gend_class.pdf

def piv_gend_class():
    tab = titanic.pivot_table('survived', index='sex', columns='class')
    # save tab as piv_gend_class.pdf

def piv_gend_class_age():
    tab = titanic.pivot_table('survived', index =['sex', age], columns='class')
    # save tab as piv_gend_class_age.pdf

def piv_gca_count():
    tab = titanic.pivot_table('survived', columns='sex', index=['class',age], aggfunc='count')
    # save tab as piv_gca_count.pdf

def fare_splice():
    fare = pd.qcut(titanic['fare'], 2)
    tab = titanic.pivot_table('survived', index=['sex',age], columns=[fare, 'class'])
    # save tab as fare_splice.pdf

def fill_zeros():
    fare = pd.qcut(titanic['fare'], 2)
    tab = titanic.pivot_table('survived', index=['sex',age], columns=[fare, 'class'], fill_value=0.0)
    # save tab as fill_zeros.pdf

if __name__=='__main__':
    heading()
    gend_surv()
    gend_class()
    piv_gend_class()
    piv_gend_class_age()
    piv_gca_count()
    fare_splice()
    fill_zeros()
