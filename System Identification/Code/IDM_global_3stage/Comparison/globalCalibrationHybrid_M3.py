# -*- coding: utf-8 -*-
"""
Created on Thu May 23 14:48:51 2024

@author: Liu
"""

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
sys.path.append("C:\\Users\\Liu\\Desktop\\HJB\\Paper\\A novel car-following model\\calibrationMethods\\BO")
from BayesianOptimizaiton import BO, feasibleRegion
from dataPreprocessing_M3_global import dataSelection_simplified, trajectory_predict_M3_global
from oneStageTools import generate_samples, latin_hypercube_sampling
import numpy as np
import pandas as pd
from SPSA import SPSA
import copy

file_path_ = "C:\\Users\\Liu\\Desktop\\HJB\\Paper\\A novel car-following model\\Case Study\\ASta_CF_data.csv"
traj_id_list_ = [0, 4, 14, 18, 27, 31]
df_selected_list_ = []
for idx in traj_id_list_:
    df_selected_ = dataSelection_simplified(file_path_, [idx])
    df_selected_list_.append(df_selected_)

def objective_func_simplified(para_list, df_selected_list = df_selected_list_):
    scales = np.array([1, 1, 10, 1, 1, 1]) 
    para_list = para_list * scales
    error = 0
    for df_selected_ in df_selected_list:
        df_results = trajectory_predict_M3_global(para_list, df_selected_)
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

def generate_search_start(init_para, global_para, update_index_list = [2, 4, 6, 7, 8]):
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

# problem_dimension = 6
# upper_bound = [3,     4,   3,     3,   3,       2]
# lower_bound = [1,     1,   2.5,   0,   0,     0.1]
# bo = BO(problem_dimension, upper_bound, lower_bound, init_sample_num = 30)
# bo.minimization(objective_func_simplified)

problem_dimension = 6
ordinal_upper_bound = [3,     4,   3,   3,   3,  1.5]
ordinal_lower_bound = [1,     1,   2.5,   0,   0,  0.1]
upper_bound = [2.8,  3.5,  3,     1.2,   3,  0.7]
lower_bound = [2.6,  3.0,  2.5,   0.8,   0,  0.3]
init_sample_num = 5
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
    upper_bound, lower_bound = update_bounds(ordinal_upper_bound, ordinal_lower_bound, samplei, fixed_index_list =[2] )
    spsa = SPSA(0.05, 0.05, upper_bound, lower_bound)
    spsa.iterations = 200
    spsa.minimization(objective_func_simplified, samplei)
    opt_para = spsa.current_opt_x
    opt_obj = objective_func_simplified(opt_para)
    print("outer loop obj value", opt_obj)
    opt_para_list.append(opt_para)
    opt_obj_list.append(opt_obj)
    ###update BO
    global_BO.X.append([samplei[j] for j in [2]])
    global_BO.Y.append(opt_obj)
    global_BO.eva_num_dict[len(global_BO.X) - 1] = global_BO.sample_eva_num
    global_BO.Lambda.append(np.var(spsa.y_list, ddof = 1)/1000000)
    df = pd.DataFrame(opt_para_list)
    df["obj"] = opt_obj_list
    df.to_csv("M3-v2.csv")   

# Result  = []
# samples = generate_samples(upper_bound, lower_bound, n = 5000)
# for samplei in samples:
#     rmse_spd, rmse_pos = objective_func_simplified(samplei)
#     re = list(samplei) + [rmse_spd, rmse_pos]
#     Result.append(re)


# iteration_count = 0
# max_iteration_num = 50
# last_opt_solution = None
# last_opt_obj_value = 5
# var_func = None
# opt_solution = None
# opt_obj_value = float("inf")
# bo = BO(problem_dimension, upper_bound, lower_bound, init_sample_num)
# while (iteration_count <= max_iteration_num):
#      print("A NEW ITERATE")
#      bo.generate_initial_samples(objective_func_simplified)
#      bo.formulate_GPR()
#      bo.formulate_EI()
#      new_sample = bo.EI.optimize_EI_func()
#      bo.update_dataset(new_sample, bo.sample_eva_num, objective_func_simplified, var_func)
#      print("BO current obj is", last_opt_obj_value)
#      if min(bo.Y) < last_opt_obj_value:
#          last_opt_obj_value = min(bo.Y)
#          current_opt_para = bo.X[np.argmin(bo.Y)]
#          print("BO current best solution is", current_opt_para, "obj is", last_opt_obj_value)
#          '''
#          update para bounds
#          '''
#          upper_bound, lower_bound = update_bounds(ordinal_upper_bound, ordinal_lower_bound, current_opt_para, fixed_index_list =[2, 4, 6, 7, 8] )

#          spsa = SPSA(0.01, 0.05, upper_bound, lower_bound)
#          spsa.iterations = 20
#          spsa.minimization(objective_func_simplified, current_opt_para)
#          current_opt_para = spsa.current_opt_x
#          if spsa.current_opt_obj_func <= opt_obj_value:
#              opt_solution = current_opt_para
#              opt_obj_value = spsa.current_opt_obj_func
             
#          upper_bound, lower_bound = update_bounds(ordinal_upper_bound, ordinal_lower_bound, current_opt_para, fixed_index_list = [0, 1, 3, 5])
#          bo = BO(problem_dimension, upper_bound, lower_bound, init_sample_num)
#          bo.upper_bound = upper_bound
#          bo.lower_bound = lower_bound
#          bo.feasible_region.upper_bound = upper_bound
#          bo.feasible_region.lower_bound = lower_bound
#          #bo.update_dataset(current_opt_para, bo.sample_eva_num, objective_func_simplified, var_func)
         




