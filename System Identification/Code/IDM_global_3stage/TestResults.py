# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 14:42:37 2024

@author: Liu
"""

import sys
sys.path.append("C:\\Users\\Liu\\Desktop\\HJB\\Paper\\A novel car-following model\\calibrationMethods\\BO")
from BayesianOptimizaiton import BO, feasibleRegion
from dataPreprocessing import dataSelection_simplified, trajectory_predict_simplified
#from Tools import generate_samples, latin_hypercube_sampling
import numpy as np
import pandas as pd
from SPSA import SPSA
import copy
from sklearn.metrics import r2_score

file_path_ = "C:\\Users\\Liu\\Desktop\\HJB\\Paper\\A novel car-following model\\Case Study\\ASta_CF_data.csv"
traj_id_list_ = [0, 4, 14, 18, 27, 31]
df_selected_list_ = []
for idx in traj_id_list_:
    df_selected_ = dataSelection_simplified(file_path_, [idx])
    df_selected_list_.append(df_selected_)

def objective_func_simplified(para_list, df_selected_list = df_selected_list_):
    scales = np.array([1, 1, 10, 1, 1, 1, 1]) 
    para_list = para_list * scales
    error = 0
    real_pos_list = []
    real_spd_list = []
    real_acc_list = []
    pred_pos_list = []
    pred_spd_list = []
    pred_acc_list = []
    for df_selected_ in df_selected_list:
        df_results =  trajectory_predict_simplified(para_list, df_selected_)
        df_results.dropna()
        pred_pos = df_results["pred_follower_pos"].tolist()
        real_pos = df_results["follower_pos"].tolist()
        pred_spd = df_results["pred_follower_spd"].tolist()
        real_spd = df_results["follower_speed"].tolist()
        pred_acc = df_results["pred_follower_acc"].tolist()
        real_acc = df_results["follower_acceleration"].tolist()
        real_pos_list = real_pos_list + real_pos
        real_spd_list = real_spd_list + real_spd
        real_acc_list = real_acc_list + real_acc
        
        pred_pos_list = pred_pos_list + pred_pos
        pred_spd_list = pred_spd_list + pred_spd
        pred_acc_list = pred_acc_list + pred_acc
        
    rmse_pos = np.sqrt(np.mean((np.array(real_pos_list) - np.array(pred_pos_list)) ** 2))
    rmse_spd = np.sqrt(np.mean((np.array(real_spd_list) - np.array(pred_spd_list)) ** 2))
    rmse_acc = np.sqrt(np.mean((np.array(real_acc_list) - np.array(pred_acc_list)) ** 2))
    pos_R_square = r2_score(real_pos_list, pred_pos_list)
    spd_R_square = r2_score(real_spd_list, pred_spd_list)
    acc_R_square = r2_score(real_acc_list, pred_acc_list)

    return rmse_pos, rmse_spd, rmse_acc, pos_R_square, spd_R_square, acc_R_square


M0_para = [2.24,3.21,2.99,1.08,1.99,0.2,0.6]
M1_para = [2.19, 2.21, 2.90, 0.74, 2.45, 0.0, 0.1]
M2_para = [2.07, 4.00, 2.82, 0.83, 2.05, 0.1, 0.1]
M3_para = [1.93, 3.60, 2.92, 0.80, 2.89, 0.0, 0.6]
re0 = objective_func_simplified(M0_para)
re1 = objective_func_simplified(M1_para)
re2 = objective_func_simplified(M2_para)
re3 = objective_func_simplified(M3_para)

















