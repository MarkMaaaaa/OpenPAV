import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import lhsmdu
import random
from scipy.stats import norm
import random
from BO_GPR import GaussianProcessRegression
from ExpectedImprovement import ExpectedImprovement



class feasibleRegion:
    def __init__ (self, dimension, upper_bound_list, lower_bound_list):
        self.dimension = dimension ##
        self.upper_bound_list = upper_bound_list
        self.lower_bound_list = lower_bound_list
        self.eva_num_dict     = {}
    
    def generate_random_points(self, sample_num):
        samples = set()
        while len(samples) < sample_num:
            sample = tuple(random.uniform(self.lower_bound_list[i], self.upper_bound_list[i]) for i in range(self.dimension))
            samples.add(sample)
        return list(samples)

class BO:
    def __init__ (self, problem_dimension, upper_bound, lower_bound, init_sample_num):
        self.problem_dimension = problem_dimension ##这个是决策变量的维度，整数类型
        self.upper_bound = upper_bound ##决策变量的上限约束，列表，表示每个维度的上限
        self.lower_bound = lower_bound ##决策变量的下限约束，列表，表示每个维度的下限
        self.init_sample_num = init_sample_num ## 算法的初始采样点数目，整数类型
        self.feasible_region = feasibleRegion(problem_dimension, upper_bound, lower_bound)
        self.l  = [10 for _ in range(self.problem_dimension)]
        self.max_sample_num = 500 ##采样的数目上限
        self.sample_eva_num = 1 ##每个采样点评估10次
        self.max_simulation_replicaiton = 500 ##仿真评估上限
        self.X = []
        self.Y = []
        self.Lambda = []
        self.GPR_list = []
        self.eva_num_dict = {}
        self.GPR = None
        self.EI  = None


        
    def func_evaluation(self, func, x):
        return func(x)
    
    def generate_initial_samples (self, func, var_func = None):
        initial_samples = self.feasible_region.generate_random_points(self.init_sample_num)
        for samplei in initial_samples:
            eva_result= []
            for evai in range(self.sample_eva_num):
                eva_result.append(self.func_evaluation(func, samplei))
            self.X.append(samplei)
            self.Y.append(np.mean(eva_result))
            self.eva_num_dict[len(self.X) - 1] = self.sample_eva_num
            if var_func == None:
                self.Lambda.append(np.var(eva_result, ddof=0))
            else:
                self.Lambda.append(var_func(samplei)/self.sample_eva_num)   
                
    def formulate_GPR(self):
        GPR = GaussianProcessRegression(self.X, self.Y, self.Lambda, self.l)
        self.GPR = GPR
        self.GPR_list.append(GPR)
    
    def formulate_EI(self):
        self.EI = ExpectedImprovement(self.X, self.Y, self.GPR, self.feasible_region)
    
    def update_dataset(self, new_x, eva_num, func, var_func = None):
        eva_result= []
        for evai in range(self.sample_eva_num):
            eva_result.append(self.func_evaluation(func, new_x))
        self.X.append(new_x)
        self.Y.append(np.mean(eva_result))
        self.eva_num_dict[len(self.X) - 1] = self.sample_eva_num
        if var_func == None:
            self.Lambda.append(np.var(eva_result, ddof=0))
        else:
            self.Lambda.append(var_func(new_x)/self.sample_eva_num)   
    
    def get_stopping_criteria(self):
        sample_num_condition = len(self.X) > self.max_sample_num
        computational_resource_condition = sum(self.eva_num_dict.values()) > self.max_simulation_replicaiton
        ill_covariance_condition = np.linalg.cond(self.GPR.Sigma_zero) > 10**16
        
        if (sample_num_condition | computational_resource_condition | ill_covariance_condition):
            return 1
        else:
            return 0
        
    def minimization (self, func, var_func = None):
        self.generate_initial_samples(func, var_func)
        stopping_criteria = 0
        while (stopping_criteria == 0):
            print("A NEW ITERATE")
            self.formulate_GPR()
            self.formulate_EI()
            new_sample = self.EI.optimize_EI_func()
            self.update_dataset(new_sample, self.sample_eva_num, func, var_func)
            stopping_criteria = self.get_stopping_criteria()
            print("CURRENT BEST SOLUTION", np.min(self.Y))
        self.optimal_solution = self.X[np.argmin(self.GPR_list[-1].mu_n_list)]
        return self.optimal_solution

      
        
        
        
    



    
    
    