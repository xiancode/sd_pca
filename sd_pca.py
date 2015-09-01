#!/usr/bin/env  Python
#-*- coding=utf-8 -*-

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sdtool import  sdtool

def data_set(fname):
    '''
    把数据转化为二维表格,每行表示一个时间段,每列表示一个指标
    删除包含空值的行
    '''
    df = pd.read_csv(fname,"\t")
    #data = df.rename(columns={'月份顺序排序':'m_order','正式指标':'indicator','正式数值':'value'})
    data = df.rename(columns={'地区':'area','正式指标':'indicator','正式数值':'value'})
    pivoted = data.pivot('area','indicator','value')
    #删除空值行
    cleaned_data = pivoted.dropna(axis=0)
    return cleaned_data

def sd_pca(fname,components=3):
    '''
    pca 计算
    '''
    cl_data = data_set(fname)
    values = cl_data.values
    pca = PCA(n_components=components)
    pca.fit(values)
    print(pca.explained_variance_)
    print(pca.explained_variance_ratio_)
    print(pca.n_components)
    
if __name__ == "__main__":
    #sd_pca("pca_rec_2014_table.txt")
    table_file_name = "table.txt"
    sdtool.rec2table("2014_1_2_season.txt", table_file_name)
    sd_pca(table_file_name)
    
    
    
    
    
    


