# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 16:17:54 2024

@author: Liu
"""
import numpy as np

def min_n_elements_and_indices(lst, n):
    # 获取排序后的列表及其索引
    sorted_indices = sorted(enumerate(lst), key=lambda x: x[1])
    
    # 提取最小的n个元素及其索引
    min_n_elements = [value for index, value in sorted_indices[:n]]
    min_n_indices = [index for index, value in sorted_indices[:n]]
    
    return min_n_elements, min_n_indices

def generate_matrix(n):
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 1
    matrix.append([0] * n)
    return matrix


#批量产生约束
def lower_bound_constraint(p):
    a = p[0]
    lower_bound = p[1]
    return {'type': 'ineq', 'fun': lambda x: x[a]-lower_bound}  
  
def upper_bound_constraint(p):
    a = p[0]
    upper_bound = p[1]
    return {'type': 'ineq', 'fun': lambda x: upper_bound-x[a]} 


def shortest_distance_to_set(vector, vector_set):
    # 将向量集合转换为 numpy 数组以便进行向量化计算
    vector_set = np.array(vector_set)
    
    # 计算向量与集合中所有向量的距离
    distances = np.linalg.norm(vector_set - vector, axis=1)
    
    # 返回最短距离
    return np.min(distances)




















