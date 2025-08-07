# -*- coding: utf-8 -*-
"""
Created on Thu May  9 21:35:27 2024

@author: Liu
"""

# -*- coding: utf-8 -*-
"""
Created on Sat May  4 11:14:38 2024

@author: Liu
"""

import sys
sys.path.append("C:\\Users\\20410\\Box\\Project\\OpenPAV\\Code\\Global Fit\\BO")
from BayesianOptimizaiton import BO, feasibleRegion
from dataPreprocessing import dataSelection_simplified, trajectory_predict_simplified
#from Tools import generate_samples, latin_hypercube_sampling
import numpy as np
import pandas as pd
from SPSA import SPSA
import copy

file_path_ = "C:\\Users\\20410\Box\\Project\\OpenPAV\Code\\Global Fit\Case\\ASta_CF_data.csv"
traj_id_list_ = [0]
df_selected_list_ = []
for idx in traj_id_list_:
    df_selected_ = dataSelection_simplified(file_path_, [idx])
    df_selected_list_.append(df_selected_)

def objective_func_simplified(para_list, df_selected_list = df_selected_list_):
    scales = np.array([1, 1, 10, 1, 1, 1, 1]) 
    para_list = para_list * scales
    error = 0
    for df_selected_ in df_selected_list:
        df_results =  trajectory_predict_simplified(para_list, df_selected_)
        pred_pos = df_results["pred_follower_pos"]
        real_pos = df_results["follower_pos"]
        pred_spd = df_results["pred_follower_spd"]
        real_spd = df_results["follower_speed"]
        pred_acc = df_results["pred_follower_acc"]
        real_acc = df_results["follower_acceleration"]
        rmse_pos = np.sqrt(np.mean((real_pos - pred_pos) ** 2))
        rmse_spd = np.sqrt(np.mean((real_spd - pred_spd) ** 2))
        rmse_acc = np.sqrt(np.mean((real_acc - pred_acc) ** 2))
        error += 100 * rmse_acc
    if error/len(df_selected_list) > 100000:
        return 100000
    else:
        return error/len(df_selected_list)

def update_bounds(ordinal_upper_bound, ordinal_lower_bound, para, fixed_index_list):
    upper_bound_ = copy.deepcopy(ordinal_upper_bound)
    lower_bound_ = copy.deepcopy(ordinal_lower_bound)
    for idx in fixed_index_list:
        upper_bound_[idx] = para[idx]
        lower_bound_[idx] = para[idx]
    return upper_bound_, lower_bound_

def generate_search_start(init_para, global_para, update_index_list = [2, 4]):
    for i in range(len(update_index_list)):
        idx = update_index_list[i]
        init_para[idx] = global_para[i]
    return init_para

def calculate_minimal_dis_to_set(point, point_list):
    min_dis = float("inf")
    for pi in point_list:
        dis =  np.linalg.norm(np.array(pi) - np.array(point))
        if dis<min_dis:
            min_dis = dis
    return min_dis



problem_dimension = 7
ordinal_upper_bound = [3,     4,   3,   3,   3,  1.5,  1.5]
ordinal_lower_bound = [1,     1,   1,   0,   0,  0.1,  0.1]
upper_bound = [2.8,  3.5,  3,     1.2,   3,  0.7,  0.7]
lower_bound = [2.0,  3.0,  2.7,   0.8,   0,  0.3,  0.3]
init_sample_num = 50
global_upper_bound = [2.8]
global_lower_bound = [3.2] 
global_problem_dimension = 1
global_BO = BO(global_problem_dimension, global_upper_bound, global_lower_bound, init_sample_num = 20)
#local_BO  = BO(problem_dimension, upper_bound, lower_bound, init_sample_num)
searchRegion = feasibleRegion(problem_dimension, upper_bound, lower_bound)
'''
首先 固定局部搜索的参数，在全局范围内进行初始化选点
'''
iteration_count = 1
max_iteration_num = 0
opt_para_list = []
opt_obj_list  = []

init_samples = searchRegion.generate_random_points(init_sample_num)
for samplei in init_samples:
    upper_bound, lower_bound = update_bounds(ordinal_upper_bound, ordinal_lower_bound, samplei, fixed_index_list =[2])
    spsa = SPSA(0.05, 0.05, upper_bound, lower_bound)
    spsa.iterations = 20
    spsa.minimization(objective_func_simplified, samplei)
    opt_para = spsa.current_opt_x
    #opt_obj  = spsa.current_opt_obj_func
    opt_obj = objective_func_simplified(opt_para)
    print("outer loop obj value", opt_obj)
    opt_para_list.append(opt_para)
    opt_obj_list.append(opt_obj)
    ###update BO
    global_BO.X.append([samplei[j] for j in [2]])
    global_BO.Y.append(opt_obj)
    global_BO.eva_num_dict[len(global_BO.X) - 1] = global_BO.sample_eva_num
    global_BO.Lambda.append(np.var(spsa.y_list, ddof = 1)/10000)
    
    df = pd.DataFrame(opt_para_list)
    df["obj"] = opt_obj_list
    df.to_csv("M0-v4.csv")

         




