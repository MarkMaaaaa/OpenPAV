# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 13:20:59 2024

@author: Liu
"""
import numpy as np
import copy
from BOTools import generate_matrix
from scipy.optimize import minimize
import random

class GaussianProcessRegression:
    def __init__ (self, X, Y, Lambda, l):
        self.X = X
        self.Y = Y
        self.Lambda = Lambda
        self.l = l
        self.Sigma_zero = None
        self.S_n_matrix = None
        self.S_n_matrix_inverse = None
        self.covariance_matrix  = None
        self.mu_n_list = None
        '''
        update information
        '''
        self.get_optimal_hyperparameter_one_dim_enumeration()
        self.update_sigma_zero_matrix()
        self.update_S_n_matrices()
        self.generate_covariance_matrix()
        self.calculate_mu_n_list()
        
    def likelihood_func(self, l):
        sample_num = len(self.X)
        K_yy = self.G_kernel(self.X, self.X, l)
        K_yy_inv = np.linalg.inv(K_yy)
        a1 = np.dot(np.array(self.Y).reshape(1, sample_num), K_yy_inv)
        a = np.dot(a1.reshape(1, sample_num), np.array(self.Y).reshape(sample_num, 1))
        b = np.log(np.linalg.det(K_yy))
        return a[0][0]+b
    
    def get_optimal_hyperparameter_one_dim_enumeration(self, lower_bound = 0.5, upper_bound = 10, search_gap = 0.2):
        sample_num = len(self.X)
        problem_dim = len(self.X[0])
        min_v = float("inf")
        for l in np.arange(lower_bound, upper_bound, search_gap):
            l_ = [l for _ in range(problem_dim)]
            K_yy = self.G_kernel(self.X, self.X, l_)
            if np.linalg.cond(K_yy) > 1e12:
                break
            K_yy_inv = np.linalg.inv(K_yy)
            a1 = np.dot(np.array(self.Y).reshape(1, sample_num), K_yy_inv)
            a = np.dot(a1.reshape(1, sample_num), np.array(self.Y).reshape(sample_num, 1))
            b = np.log(np.linalg.det(K_yy))
            if abs(a + b) < min_v:
                min_v = a + b
                self.l = l_
    
    def get_optimal_hyperparameter_multi_dim(self, lower_bound = 0.1, upper_bound = 20, multi_start = 5):
        print("gggg")
        problem_dim = len(self.X[0])
        print("gggg")
        lower_bound_list = [lower_bound for _ in range(problem_dim)]
        upper_bound_list = [upper_bound for _ in range(problem_dim)]
        min_func_value   = float("inf")
        print("gggg")
        for _ in range(multi_start):
            print("new iterate")
            l_sample = tuple(random.uniform(lower_bound_list[i], upper_bound_list[i]) for i in range(problem_dim))
            result = minimize(self.likelihood_func, l_sample)
            if result.fun < min_func_value:
                min_func_value = result.fun
                self.l         = result.x  
                
    def G_kernel(self, x1, x2, l):
        len1 = len(x1)
        len2 = len(x2)
        K = np.zeros([len1, len2])
        for i in range(len(x1)):
            for j in range(len(x2)):
                dis = np.linalg.norm((np.array(x1[i]) - np.array(x2[j]))/np.array(l))
                K[i][j] = dis
        return np.exp(-0.5 * K ** 2)

    def update_sigma_zero_matrix(self):
        self.Sigma_zero = self.G_kernel(self.X, self.X, self.l)  
    
    def update_S_n_matrices(self):
        self.S_n_matrix   = copy.deepcopy(self.Sigma_zero)
        for idx in range(len(self.Lambda)):
            self.S_n_matrix[idx][idx] += self.Lambda[idx]
        self.S_n_matrix_inverse = np.linalg.inv(self.S_n_matrix)

    def generate_covariance_matrix(self):
        self.covariance_matrix = self.Sigma_zero - np.dot(self.Sigma_zero, np.dot(self.S_n_matrix_inverse, self.Sigma_zero))
        
    def generate_persudo_covariance_matrix(self, new_x):
        '''
        返回由(x1，..,x_n,new_x)组成的协方差矩阵

        '''
        new_X_list = copy.deepcopy(self.X)
        new_X_list.append(new_x)
        Sigma_zero_new = self.G_kernel(new_X_list, new_X_list, self.l)
        ##gengerate n+1 * n matrix
        I_matrix = generate_matrix(len(self.X))
        Sigma_zero_multip_I = np.dot(Sigma_zero_new, I_matrix)
        return Sigma_zero_new - np.dot(Sigma_zero_multip_I, np.dot(self.S_n_matrix_inverse, Sigma_zero_multip_I.T))
    
    def calculate_mu_n_list(self):
        '''
        
        计算已有采样点目标函数值的估计均值

        '''
        len_Y = len(self.Y)
        mu_n_list_ = np.dot(self.Sigma_zero, np.dot(self.S_n_matrix_inverse, np.array(self.Y).reshape(len_Y, 1)))
        self.mu_n_list = mu_n_list_.flatten().tolist()
    
    def estimate_mu_n(self, new_x):
        '''
        高斯过程估计目标函数值
        '''
        len_Y = len(self.Y)
        K_vector = self.G_kernel([new_x], self.X, self.l)
        estimated_mu_n =  np.dot(K_vector.reshape(1, len_Y), np.dot(self.S_n_matrix_inverse, np.array(self.Y).reshape(len_Y, 1)))
        return estimated_mu_n.flatten()[0]
    
    def estimate_conditional_var(self, new_x):
        '''
        高斯过程估计不确定性
        '''
        len_Y = len(self.Y)
        unconditional_var = self.G_kernel([new_x], [new_x], self.l)
        K_vector = self.G_kernel([new_x], self.X,  self.l)
        estimated_var =  unconditional_var - np.dot(K_vector.reshape(1, len_Y), np.dot(self.S_n_matrix_inverse, K_vector.reshape(len_Y, 1)))
        return estimated_var[0][0]
    
    def estimate_mu_n_list(self, new_x, lambda_new_x):
        '''
        给出新增采样点，在实际仿真之前估计mu_n_list 的可能值，返回a_list 和 b_list
        a_list为估计所得的mu_n_list
        b_list为Scott论文最后一列
        '''
        persudo_cov_matrix = self.generate_persudo_covariance_matrix(new_x)
        mu_n_of_new_x = self.estimate_mu_n(new_x)
        factor = 1/(lambda_new_x + persudo_cov_matrix[-1][-1])**(1/2)
        original_mu_n_list = copy.deepcopy(self.mu_n_list)
        original_mu_n_list.append(mu_n_of_new_x)
        return original_mu_n_list, (persudo_cov_matrix[-1]*factor).tolist()
        
    def update_mu_n_list_based_on_new_obervation(self, new_x, y_pred, lambda_new_x):
        '''
        给定实际的观测值y_pred,估计新的mu_n_list分布
        '''
        persudo_cov_matrix = self.generate_persudo_covariance_matrix(new_x)
        mu_n_of_new_x = self.estimate_mu_n(new_x)
        factor = (y_pred - mu_n_of_new_x)/(lambda_new_x + persudo_cov_matrix[-1][-1])
        original_mu_n_list = copy.deepcopy(self.mu_n_list)
        original_mu_n_list.append(mu_n_of_new_x)
        return np.array(original_mu_n_list) + persudo_cov_matrix[-1]*factor     
        
# X1 = [[1], [2], [3]]
# Y1 = [1, 3, 6]
# Lambda1 = [1,1,2]
# l  = 2

# GP1 = GaussianProcessRegression(X1, Y1, Lambda1, l)
# new_mu_list = GP1.update_mu_n_list_based_on_new_obervation( [1.5], 4, 2)

# #a_list, b_list = GP1.estimate_mu_n_list([1.5], 2)

# X2 = [[1], [2], [3], [1.5]]
# Y2 = [1, 3, 6, 4]
# Lambda2 = [1,1,2,2]
# l  = 1
# GP2 = GaussianProcessRegression(X2, Y2, Lambda2, l)    
# new_mu_list_ = GP2.mu_n_list     
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        