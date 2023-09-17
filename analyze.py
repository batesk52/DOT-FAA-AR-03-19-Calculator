# -*- coding: utf-8 -*-
"""
:::::::::::::::::::NOTEPAD:::::::::::::::::::

    

this is the code I will use to make a multi-index similar to the one I see on AGATE document
pd.MultiIndex.from_product([['RTD','ETD','ETW','CTD'],["SI",'Imperial']])
ind=pd.MultiIndex.from_product(["Material 1","Material 2"],["Max","Mean","Min","CoV
ind=pd.MultiIndex.from_product(["Material 1","Material 2"],["Max","Mean","Min","CoV","A-Basis","B-Basis"]])
ind=pd.MultiIndex.from_product([["Material 1","Material 2"],["Max","Mean","Min","CoV","A-Basis","B-Basis"]])
ind
results = pd.DataFrame(data_clean,index=ind,columns=col)
results = pd.DataFrame(data_clean,index=ind,columns=cols)




"""

"""
______________________________________________________________________________
_________________     Class for Data Collected from Summary      __________________
______________________________________________________________________________

"""  


import scipy
from scipy import stats
from scipy.stats import mannwhitneyu


class Stats(object):
    def __init__(self): 
        pass
    
    import pandas as pd
    import math
    import os
    import scipy
    from scipy import stats
    from scipy.stats import mannwhitneyu
    import numpy as np
    from matplotlib import pyplot as plt
    
    def basis_approx(self,results,basis):
        try:  
            # drop units from imported data, if they exist  
            test_data=results
            # get test names from keys of raw data dictionary
            testname=list(test_data.index) 
            n=len(testname)
            if n<3:
                return "N/A"
            f=n-2
            if basis=="a":
                z=2.32635
                if f<3:
                    q=0.05129
                else:
                    q=f-2.327*(f**.5)+1.138+0.6057*(f**.5)**-1-0.3287*f**-1
                b=2.0643*(f**.5)**-1-0.95145*f**-1+0.51251*(f*(f**.5))**-1
                c=0.36961+0.0026958*(f**.5)**-1-0.65201*f**-1+0.011320*(f*(f**.5))**-1
                k=z*(f/q)**.5+((c*n)**-1+(b/2/c)**2)**.5-b/2/c
                # B-Basis Calculation:
                basis_val=test_data.mean()-k*test_data.std()
    
            elif basis=="b":
                z=1.28
                if f<3:
                    q=0.05129
                else:
                    q=f-2.327*(f**.5)+1.138+0.6057*(f**.5)**-1-0.3287*f**-1
                b=1.1372*(f**.5)**-1-0.49162*f**-1+0.18612*(f*(f**.5))**-1
                c=0.36961+0.0040342*(f**.5)**-1-0.7175*f**-1+0.19693*(f*(f**.5))**-1
                k=z*(f/q)**.5+((c*n)**-1+(b/2/c)**2)**.5-b/2/c
                # B-Basis Calculation:
                basis_val=test_data.mean()-k*test_data.std()
                
            results_df=self.pd.DataFrame({f"{basis}-basis":basis_val,
                                        "Mean":test_data.mean(),
                                        "Standard Deviation":test_data.std(),
                                        "Sample Size (n)":n,
                                        "Degree of Freedom (f)":f,
                                        "Q":q,
                                        f"z_{basis}":z,
                                        f"b factor (b_{basis})":b,
                                        f"c factor (c_{basis})":c,
                                        "k factor":k},index=[0]).transpose().round(3)
            return basis_val
        except:
            return "N/A"
    
    
    def compare_means(self,data_a,data_b):   
        test_data_a=data_a
        test_data_b=data_b
        # calculate mean, std deviation 
        mean_a = test_data_a.mean().values
        mean_b = test_data_b.mean().values
        stdev_a=test_data_a.std().values
        stdev_b=test_data_b.std().values
        
        #perform, shapiro wilks test for normality on data_a & data_b
        t_score_sw_a,p_value_sw_a = self.scipy.stats.shapiro(test_data_a)
        if float(p_value_sw_a)<0.05:
            sw_a_res="Assumption of Normality Rejected for Dataset A"
        else:
            sw_a_res="Assumption of Normality NOT Rejected for Dataset A"
        
        t_score_sw_b,p_value_sw_b = self.scipy.stats.shapiro(test_data_b)
        if float(p_value_sw_b)<0.05:
            sw_b_res="Assumption of Normality Rejected for Dataset B"
        else:
            sw_b_res="Assumption of Normality NOT Rejected for Dataset B"            
        
        if p_value_sw_a < 0.05 or p_value_sw_b < 0.05: # if either dataset is not normal,
                                               # use Mann-Whitney test
            
            print("Data A type:", test_data_a.dtypes)
            print("Data B type:", test_data_b.dtypes)

            
            test_run = "Perform Mann-Whitney U-Test (one or both datasets not normally distributed)"
            stat_mw, p_value_mw = mannwhitneyu(test_data_a.to_numpy(),
                                                    test_data_b.to_numpy(),
                                                    alternative='two-sided')
            
            if float(p_value_mw) < 0.05:
                test_result = "Reject Null Hypothesis; difference in mean is statistically significant."
            else:
                test_result = "Cannot reject null hypothesis; difference in mean is statistically insignificant."   
            
            results_df=self.pd.DataFrame({"A - Mean":mean_a,
                                          "A - Std Dev":stdev_a,
                                          "A - Shapiro Willks P Value":p_value_sw_a,
                                          "A - Normality Determination":sw_a_res,
                                          "B - Mean":mean_b,
                                          "B - Std Dev":stdev_b,
                                          "B - Shapiro Willks P Value":p_value_sw_b,
                                          "B - Normality Determination":sw_b_res,
                                          "Analysis Performed":test_run,
                                          "Test Statistic":stat_mw,
                                          "p value":p_value_mw,
                                          "Determination":test_result,
                                          },index=["Results"]).transpose().round(3)
            
            
        else: # if the assumption of normality is not violated, use a student-t or welch test
    
            # perform levine test to determine if homogeneity of variance is voilated
            t_score_l,p_value_l = self.scipy.stats.levene(test_data_a.values.flatten(),
                                                          test_data_b.values.flatten())
            # if the null can be rejected, perform Welch's t-test
            if float(p_value_l) < 0.05:
                levene_res = "Reject null hypothesis; homogeneity of variance is invalid."
                test_run = "Perform Welch's t-test (unequal variance)"
                t_score,p_value=self.scipy.stats.ttest_ind(test_data_a,
                                                             test_data_b,equal_var=False)
            # if the null cannot be rejected, run student's t-test
            else:
                levene_res = "Do not reject null hypothesis; homogeneity of variance is valid."
                test_run = "Perform Student's t-test (equal variance)"   
                t_score,p_value=self.scipy.stats.ttest_ind(test_data_a,
                                                             test_data_b,equal_var=True) 
            if float(p_value) < 0.05:
                test_result = "Reject Null Hypothesis; difference in mean is statistically significant."
            else:
                test_result = "Cannot reject null hypothesis; difference in mean is statistically insignificant."
                
            results_df=self.pd.DataFrame({"A - Mean":mean_a,
                                          "A - Std Dev":stdev_a,
                                          "A - Shapiro Willks P Value":p_value_sw_a,
                                          "A - Normality Determination":sw_a_res,
                                          "B - Mean":mean_b,
                                          "B - Std Dev":stdev_b,
                                          "B - Shapiro Willks P Value":p_value_sw_b,
                                          "B - Normality Determination":sw_b_res,
                                          "Levene Test (variance check)":p_value_l,
                                          "Result":levene_res,
                                          "Analysis Performed":test_run,
                                          "Test Statistic":t_score,
                                          "p value":p_value,
                                          "Determination":test_result,
                                          },index=["Results"]).transpose().round(3)
                
        return results_df

"""
______________________________________________________________________________
_________________     Class for Data from "Input Data"       __________________
______________________________________________________________________________

"""

class Allowables(Stats):
    def __init__(self):
        pass
    
    import pandas as pd
    import math
    import os
    import scipy
    from scipy import stats
    import numpy as np
    from matplotlib import pyplot as plt
    

    # example: should we first organize the data by condition, method, or what?
    
    
    # this code is for performing calculations on dataframes 
    # they will be called by create_report.py function for specific things
    
    def summary(self,data):
        data_all, data_sub={},{} #creating nested dictionaries to store data:
        mat_property={} # create dictionary to save files
        materials=data.keys()
        i=0
        for material in materials:
            mat_property[material]=data[material].keys()
            for prop in mat_property[material]:
                 # creates a per-material, per-property summary of all the results
                data_sub[prop] = data[material][prop].iloc[:,1:-2].groupby(["Condition",
                                                                            "Method"]).agg(["max",
                                                                                            "mean",
                                                                                            "min",
                                                                                            "std",
                                                                                            "count"])
                #saving all the results of the summary
                # into the master dictionary, using material name as key
                data_all[material]=data_sub
            data_sub={} #empty dataframe for rewritting later
            i+=1
        return data_all


    def a_b_basis(self,data,parameters):
        def summ(x):
            result = {
                'Mean': x["Value (SI)"].mean(),
                'Minimum': x["Value (SI)"].min(),
                'Maximum': x["Value (SI)"].max(),
                'CoV (%)': x["Value (SI)"].std() / x["Value (SI)"].mean() *100,
                "B-Basis": self.basis_approx(x["Value (SI)"],"b"),
                "A-Basis": self.basis_approx(x["Value (SI)"],"a"),
                "# Specimens": x["Value (SI)"].count()
            }
            return pd.Series(result)
        
        data_all, data_sub={},{} #creating nested dictionaries to store data:
        mat_property={} # create dictionary to save files
        materials=data.keys()
        i=0
        for material in materials:
            mat_property[material]=data[material].keys()
            for prop in mat_property[material]:
                 # creates a per-material, per-property summary of all the results
                data_sub[prop] = data[material][prop].iloc[:,1:-2].groupby(parameters).apply(summ).transpose()
                #saving all the results of the summary
                # into the master dictionary, using material name as key
                data_all[material]=data_sub
            data_sub={} #empty dataframe for rewritting later
            i+=1
        return data_all

    def DOT_FAA_AR_03_019(self,data):
        pass # I want to copy / paste this exactly, and have the results output to a report
    
"""
______________________________________________________________________________
__________________          Class - Plot Results            ___________________
______________________________________________________________________________

"""  

# Imports    
import pandas as pd
import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt
import scipy.stats as stats

class Plot():
    
    def __init__(self, fig=None, ax=None):
        
        if (fig == None) or (ax == None):
            self.fig, self.ax = plt.subplots(figsize=(10,8)) # create figure & axes
        else:
            self.fig = fig
            self.ax = ax

class Line_plot(Plot):
    
    def __init__(self, x_col_name, y_col_name, **kwargs):
        
        self.x_col_name = x_col_name
        self.y_col_name = y_col_name
        
        super().__init__(**kwargs)
    
    def add_test(self, test, **kwargs):
        
        l = self.ax.plot(test[self.x_col_name], test[self.y_col_name], **kwargs)
    
        return l
        
    def add_tests(self, tests, **kwargs):
        
        l = []
        
        for test in tests:
            l.append(self.add_test(tests[test], **kwargs))
            
        return l

