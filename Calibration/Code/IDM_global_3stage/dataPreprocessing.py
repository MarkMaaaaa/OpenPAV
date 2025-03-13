# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 14:25:36 2024

@author: Liu
"""
import pandas as pd
import warnings
import random


'''
Define the IDM model
'''
def s_star_func(follower_speed, speed_diff, desired_dec, desired_acc, safty_time_gap, jam_spacing):
    return jam_spacing + follower_speed * safty_time_gap + follower_speed * speed_diff/(2 * (desired_acc * desired_dec)**(1/2))

def IDM_model (pos_diff, speed_diff, follower_speed, desired_acc, desired_dec, desired_speed, safty_time_gap, jam_spacing, delta):
    '''
    Parameters to be determined including: desired_acc, desired_dec, desired_speed, safty_time_gap, jam_spacing, delta
    safty time gap is T
    jam_spacing is s_0 
    '''
    speed_diff_ = -speed_diff
    s_star = s_star_func(follower_speed, speed_diff_, desired_dec, desired_acc, safty_time_gap, jam_spacing)
    factor = 1 - (follower_speed/desired_speed)**delta  - (s_star/pos_diff)**2
    return factor * desired_acc

    
        

'''
data preprocessing
'''

def dataSelection(file_path, traj_id_list):
    #df = pd.read_csv(file_path, skiprows=0, nrows=300000)
    df = pd.read_csv(file_path)
    df_selected = df[df["traj_id"].isin(traj_id_list)]
    #df_selected = dataFiltering(df_selected)
    return df_selected

def dataSelection_simplified(file_path, traj_id_list):
    df_selected_ = dataSelection(file_path, traj_id_list)
    df_selected_["pos_diff"] = df_selected_["leader_pos"] - df_selected_["follower_pos"]
    df_selected_["spd_diff"] = df_selected_["leader_speed"] - df_selected_["follower_speed"]
    df_selected_ = df_selected_.dropna()
    return df_selected_

def trajectory_predict_simplified(parameter_list, df_selected_, start_index = 7000, end_index = 70000, delta_t = 0.1):
    warnings.filterwarnings("ignore")
    desired_acc    = parameter_list[0]
    desired_dec    = parameter_list[1]
    desired_speed  = parameter_list[2]
    safty_time_gap = parameter_list[3]
    jam_spacing    = parameter_list[4]
    delta          = 4
    eta_a          = parameter_list[5]
    eta_b          = parameter_list[6]
    control_time_interval = 0.01
    df_selected_ = df_selected_.reset_index(drop=True)
    # #start_index   = random.randint(0, 1000)
    # start_index    = random.randint(0,2)
    # end_index    = start_index + 1000
    for index, row in df_selected_.iloc[start_index-100: end_index].iterrows(): ##减100以防eta_a 过大
        if index <= start_index:
            df_selected_.at[index, "pred_pos_diff"] = row["pos_diff"]
            df_selected_.at[index, "pred_spd_diff"] = row["spd_diff"]
            df_selected_.at[index, "pred_follower_pos"] = row["follower_pos"]
            df_selected_.at[index, "pred_follower_spd"] = row["follower_speed"]
            df_selected_.at[index, "pred_follower_acc"] = row["follower_acceleration"]
        if index >= start_index:
            pos_diff_before_eta_a = df_selected_.at[index - int(eta_a/delta_t), "pred_pos_diff"]
            spd_diff_before_eta_a = df_selected_.at[index - int(eta_a/delta_t), "pred_spd_diff"]
            follower_spd_before_eta_a = df_selected_.at[index - int(eta_a/delta_t), "pred_follower_spd"]
            command_acc = IDM_model(pos_diff_before_eta_a, spd_diff_before_eta_a, follower_spd_before_eta_a, desired_acc, 
                                    desired_dec, desired_speed, safty_time_gap, jam_spacing, delta)
            factor = delta_t/eta_b
            df_selected_.at[index+1, "pred_follower_acc"] = (1-factor) * df_selected_.at[index, "pred_follower_acc"] + factor * command_acc
            df_selected_.at[index+1, "pred_follower_spd"] = df_selected_.at[index , "pred_follower_spd"] + delta_t * df_selected_.at[index, "pred_follower_acc"]
            df_selected_.at[index+1, "pred_follower_pos"] = df_selected_.at[index,"pred_follower_pos"] + df_selected_.at[index,"pred_follower_spd"] * delta_t + 0.5 *  df_selected_.at[index,"pred_follower_acc"] * delta_t**2

            df_selected_.at[index+1, "pred_pos_diff"] = df_selected_.at[index+1, "leader_pos"] - df_selected_.at[index+1, "pred_follower_pos"]
            df_selected_.at[index+1, "pred_spd_diff"] = df_selected_.at[index+1, "leader_speed"] - df_selected_.at[index+1, "pred_follower_spd"]
    '''
    calculate errors
   
    real_pos = df_selected_["follower_pos"]
    pred_pos = df_selected_["pred_follower_pos"]
    real_acc = df_selected_["follower_acceleration"]
    pred_acc = df_selected_["pred_follower_acc"]
    real_speed = df_selected_["follower_speed"]
    pred_speed = df_selected_["pred_follower_spd"]
    rmse_pos = np.sqrt(np.mean((real_pos - pred_pos) ** 2))
    rmse_acc = np.sqrt(np.mean((real_acc - pred_acc) ** 2))
    rmse_speed = np.sqrt(np.mean((real_speed - pred_speed) ** 2))
    '''
    return df_selected_.dropna()






