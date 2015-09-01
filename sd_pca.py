#!/usr/bin/env  Python
#-*- coding=utf-8 -*-

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn import preprocessing
from sdtool import  sdtool

#global area_list

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
    area_list = pivoted.index
    return cleaned_data,area_list

def sd_pca(fname,components=2):
    '''
    pca 计算
    '''
    cl_data,area_list = data_set(fname)
    values = cl_data.values
    pca = PCA(n_components=components)
    #数据标准化
    values = preprocessing.scale(values)
    pca.fit(values)
    
    print(pca.explained_variance_)
    print(pca.explained_variance_ratio_)
    print(pca.n_components)
    print(pca.components_)
    scores = np.dot(pca.transform(values),pca.explained_variance_ratio_)
    #print scores
    scores_list = scores.tolist()
    result_col =  cl_data.columns
    result_col.name = "指标"
    result_idx = ["主成分"+str(i+1) for i in range(components)]
    result_data = pd.DataFrame(pca.components_,columns=result_col,index=result_idx)
    #result_data = result_data.astype(float)
    result_data.to_csv("pca_result.txt",sep="\t",float_format='%8.4f')
    #
    fout = open("pca_result.txt","a")
    fout.write("\n===============================\n")
    if len(area_list) == len(scores):
        area_scores = zip(scores_list,area_list)
        as_dict = dict((key,value) for key,value in area_scores)
        #order by scores
        #scores.sort
        scores_list.sort(reverse=True)
        for score in scores_list:
            #print area_list[i],scores[i]
            fout.write("%s,%.5f \n" % (as_dict[score],score))
    else:
        print "caculated result not equal to area_list"
    fout.close()
    print "save to pca_result.txt"
    
    
if __name__ == "__main__":
    #sd_pca("pca_rec_2014_table.txt")
    table_file_name = "table.txt"
    sdtool.rec2table("season_2014_season_1_2_rec.txt", table_file_name)
    sd_pca(table_file_name)
    
    
    
    
    
    


