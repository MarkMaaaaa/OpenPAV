# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 21:51:23 2024

@author: Liu
"""

from BO_GPR import GaussianProcessRegression
import numpy as np
from scipy.stats import norm
from BOTools import lower_bound_constraint
from BOTools import upper_bound_constraint, shortest_distance_to_set
from scipy.optimize import minimize

class ExpectedImprovement:
    def __init__ (self, X, Y, GPR, feasible_region):
        self.X = X
        self.Y = Y
        self.feasible_region = feasible_region
        self.GPR = GPR
        self.multi_start = 10
    
    def calculate_EI_value(self, new_x):
        mean = self.GPR.estimate_mu_n(new_x)
        conditional_var = self.GPR.estimate_conditional_var(new_x)
        std = conditional_var**(1/2)
        
        y_star = min(self.Y)
        component = (y_star - mean )/std
        EI_value = (y_star - mean) * norm.pdf(component, 0, 1) + std * norm.cdf(component, 0, 1)
        return -EI_value
    
    def _generate_constraints(self):
        lower_bound_map = []
        upper_bound_map = []
        for a in range(self.feasible_region.dimension):
            lower_bound_map.append((a, self.feasible_region.lower_bound_list[a]))
            upper_bound_map.append((a, self.feasible_region.upper_bound_list[a]))
        lower_con_set=list(map(lower_bound_constraint,lower_bound_map))   
        upper_con_set=list(map(upper_bound_constraint,upper_bound_map))
        return lower_con_set + upper_con_set

    def generate_feasible_index(self, optimal_new_x):
        feasible_index = 1
        if optimal_new_x is None:
            feasible_index = 0
            return feasible_index
        elif any (item is None for item in optimal_new_x):
            feasible_index = 0 
            return feasible_index
        if shortest_distance_to_set(optimal_new_x, self.X) < 1e-3:
            feasible_index = 0 
            return feasible_index
        return feasible_index

    def check_final_solution(self, optimal_new_x):
        while self.generate_feasible_index(optimal_new_x) == 0:
            optimal_new_x = None
            minimal_EI_value = float("inf")
            random_samples = self.feasible_region.generate_random_points(self.multi_start)
            for xi in random_samples:
                EI_value = self.calculate_EI_value(xi)
                if EI_value < minimal_EI_value:
                    minimal_EI_value = EI_value
                    optimal_new_x = xi
        return optimal_new_x

    def optimize_EI_func(self):
        search_starts = self.feasible_region.generate_random_points(self.multi_start)
        interval_constraint = self._generate_constraints()
        optimal_new_x = None
        minimal_EI_value = float("inf")
        for idx in range(self.multi_start):
            x_t = search_starts[idx]
            res = minimize(self.calculate_EI_value, x_t, constraints=interval_constraint)
            EI_value = self.calculate_EI_value(res.x)
            if EI_value < minimal_EI_value:
                minimal_EI_value = EI_value
                optimal_new_x = res.x
        optimal_new_x = self.check_final_solution(optimal_new_x)
        return optimal_new_x
    