# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 13:39:29 2024

@author: Liu
"""
import random
import numpy as np

def generate_samples(upper_bound_list, lower_bound_list, n):
    samples = []
    for _ in range(n):
        sample = []
        for upper_bound, lower_bound in zip(upper_bound_list, lower_bound_list):
            sample.append(random.uniform(lower_bound, upper_bound))
        samples.append(sample)
    return samples



def latin_hypercube_sampling(upper_bound_list, lower_bound_list, sample_number):
    dim = len(upper_bound_list)
    samples = np.zeros((sample_number, dim))

    # 生成拉丁超立方采样
    for i in range(dim):
        boundaries = np.linspace(lower_bound_list[i], upper_bound_list[i], num=sample_number + 1)
        offset = np.random.uniform(0, 1, sample_number)
        for j in range(sample_number):
            samples[j, i] = boundaries[j] + offset[j] * (boundaries[j + 1] - boundaries[j])

    return samples

# # 输入参数
# upper_bound_list = [10, 20, 30]  # 上界列表
# lower_bound_list = [1, 5, 10]    # 下界列表
# sample_number = 5                # 采样点数量

# # 生成采样点
# samples = latin_hypercube_sampling(upper_bound_list, lower_bound_list, sample_number)

# # 输出采样点
# print("采样点：")
# print(samples)
