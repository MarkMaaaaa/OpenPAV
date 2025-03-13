# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 10:26:02 2024

@author: Liu
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 14:25:36 2024

@author: Liu
"""
import pandas as pd
import warnings


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

def trajectory_predict_M1_global(parameter_list, df_selected_, start_index = 100, end_index = 7000, delta_t = 0.1):
    warnings.filterwarnings("ignore")
    desired_acc    = parameter_list[0]
    desired_dec    = parameter_list[1]
    desired_speed  = parameter_list[2]
    safty_time_gap = parameter_list[3]
    jam_spacing    = parameter_list[4]
    delta          = 4
    eta_a          = 0
    eta_b          = 0.1
    df_selected_["pos_diff"] = df_selected_["leader_pos"] - df_selected_["follower_pos"]
    df_selected_["spd_diff"] = df_selected_["leader_speed"] - df_selected_["follower_speed"]
    df_selected_ = df_selected_.dropna()
    df_selected_ = df_selected_.reset_index(drop=True)
    for index, row in df_selected_.iloc[start_index-100: end_index].iterrows():
        if index <= start_index:
            df_selected_.at[index, "pred_pos_diff"] = row["pos_diff"]
            df_selected_.at[index, "pred_spd_diff"] = row["spd_diff"]
            df_selected_.at[index, "pred_follower_pos"] = row["follower_pos"]
            df_selected_.at[index, "pred_follower_spd"] = row["follower_speed"] 
            df_selected_.at[index, "pred_follower_acc"] = row["follower_acceleration"]
        if index >= start_index:
            pos_diff = df_selected_.at[index, "pred_pos_diff"]
            spd_diff = df_selected_.at[index, "pred_spd_diff"]
            follower_spd = df_selected_.at[index, "pred_follower_spd"]
            command_acc = IDM_model(pos_diff, spd_diff, follower_spd, desired_acc, 
                                    desired_dec, desired_speed, safty_time_gap, jam_spacing, delta)
            factor = delta_t/eta_b
            df_selected_.at[index+1, "pred_follower_acc"] = (1-factor) * df_selected_.at[index, "pred_follower_acc"] + factor * command_acc
            df_selected_.at[index+1, "pred_follower_spd"] = df_selected_.at[index , "pred_follower_spd"] + delta_t * df_selected_.at[index, "pred_follower_acc"]
            df_selected_.at[index+1, "pred_follower_pos"] = df_selected_.at[index,"pred_follower_pos"] + df_selected_.at[index,"pred_follower_spd"] * delta_t + 0.5 *  df_selected_.at[index,"pred_follower_acc"] * delta_t**2

            df_selected_.at[index+1, "pred_pos_diff"] = df_selected_.at[index+1, "leader_pos"] - df_selected_.at[index+1, "pred_follower_pos"]
            df_selected_.at[index+1, "pred_spd_diff"] = df_selected_.at[index+1, "leader_speed"] - df_selected_.at[index+1, "pred_follower_spd"]
    return df_selected_