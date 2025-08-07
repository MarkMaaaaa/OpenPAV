# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 21:46:28 2024

@author: Liu
"""
import numpy as np
import copy
class SPSA:
    def __init__(self, step_length, pertubation_factor, upper_bound_list, lower_bound_list):
        self.step_length = step_length
        self.pertubation_factor = pertubation_factor
        self.iterations = 1000 ## default interation number is 1000
        self.upper_bound_list = upper_bound_list
        self.lower_bound_list = lower_bound_list
        self.x_list = []
        self.y_list = []
        self.gradient_list = []
        self.current_opt_x = None
        self.current_opt_obj_func = float("inf")
        
    def minimization(self, func, x_init):
        x = np.copy(x_init)
        n_params = len(x)
        delta = self.pertubation_factor
        for k in range(self.iterations):
            # 随机扰动
            delta_k = 2 * np.random.randint(0, 2, size=(n_params,)) - 1
            
            # 计算扰动点
            x_plus = x + delta * delta_k
            x_minus = x - delta * delta_k
            
            # 计算函数值
            y_plus = func(x_plus)
            y_minus = func(x_minus)
            
            # 计算梯度估计
            g = (y_plus - y_minus) / (2 * delta * delta_k)
            # 更新参数
            x -= self.step_length / (k + 1)**0.1667 * g
            ##检查是否超出约束范围：
            for i in range(len(self.upper_bound_list)):
                ubi = self.upper_bound_list[i]
                lbi = self.lower_bound_list[i]
                if x[i] < lbi:
                    x[i] = lbi
                if x[i] > ubi:
                    x[i] = ubi
            ##计算当前解的目标函数值
            y_ = func(x)
            self.current_x = x
            self.current_gradient = g
            self.x_list.append(x)
            self.y_list.append(y_)
            self.gradient_list.append(g)
            if self.current_opt_obj_func > y_:
                self.current_opt_x = copy.deepcopy(x)
                self.current_opt_obj_func = copy.deepcopy(y_)
            
            #print("current x is", x)
            print("SPSA current opt objective function is", func(self.current_opt_x))
        return self.current_opt_x