# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 21:46:07 2021

@author: Robert Janjic
"""

import numpy as np
import matplotlib.pyplot as plt


n = pow(10,4)         # number of agents
t = 50                # number of periods
init_w = 10           # the initial wealth of firms (same for all)

var_list = np.arange(0.1, 3.1, 0.1)     # list of possible variances
num_vars = len(var_list)              # number of different variances used
var_constant = True                   # when True, variance stays the same for the agent throughout time; when False, variance gets redrawn every period

death_zone = 0.05     # this will be the percentage of firms on the lower end of the size distribution (in every round) that will receive a strike
max_strikes = 4       # after collecting this many strikes in a row, a firm dies
strike_counter = np.zeros((n, t))

death_thresh = 0    # when wealth reaches this level, the firm dies

w = np.zeros((n, t, 2))     # agent n, in period t, with w(ealth) and var(iance)

w[:,0,0] = init_w           # set up all agents with same inital wealth

# initialize every agent with a variance
var_list_index = 0
for i in range(n):
    var = var_list[var_list_index]
    w[i,0,1] = var
    if var_list_index < num_vars-1:
        var_list_index += 1
    else:
        var_list_index = 0


for j in range(1, t):
    for i in range(n):
        if w[i,j-1,0] > death_thresh:
            w[i,j,0] = w[i,j-1,0] + np.random.normal(0, w[i,j-1,1])
            
        if var_constant:
            w[i,j,1] = w[i,j-1,1]
        else:
            w[i,j,1] = w[i,j-1,1]       # ATTENTION: redrawing variances is not implemented yet
        
        if w[i,j,0] <= death_thresh:
            w[i,j,0] = death_thresh
    
    current_round = np.copy(w[:,j,0])
    current_round[current_round == 0] = pow(10,10)
    current_ranking = np.argsort(current_round)
    for k in range(int(death_zone*n)):
        index = current_ranking[k]
        strike_counter[index,j] = strike_counter[index,j-1] + 1
        if strike_counter[index,j] == max_strikes:
            w[index,j,0] = 0
    
# Calculating means per variance-type
means = np.zeros((num_vars,t))

for j in range(t):
    current_period = w[:,j]
    for k in range(num_vars):
        type_list = current_period[current_period[:,1] == var_list[k]]
        mean = np.mean(type_list[:,0])
        means[k,j] = mean

# Calculate mean wealth for every quartile of variances - Plot 1
mean_Q1 = np.mean(means[:int(num_vars/4)], axis=0)
mean_Q2 = np.mean(means[int(num_vars/4):2*int(num_vars/4)], axis=0)
mean_Q3 = np.mean(means[2*int(num_vars/4):3*int(num_vars/4)], axis=0)
mean_Q4 = np.mean(means[3*int(num_vars/4):], axis=0)

result_matrix = np.vstack((mean_Q1, mean_Q2, mean_Q3, mean_Q4))

# =============================================================================
# #Calculate dead firms for every round - Plot 2
# Q1 = var_list[:int(num_vars/4)]
# Q2 = var_list[int(num_vars/4):2*int(num_vars/4)]
# Q3 = var_list[2*int(num_vars/4):3*int(num_vars/4)]
# Q4 = var_list[3*int(num_vars/4):]
# 
# group_Q1 = []
# group_Q2 = []
# group_Q3 = []
# group_Q4 = []
# 
# for j in range(t):
#     current_period = w[:,j]
#     for k in range(num_vars):
#         type_list = current_period[current_period[:,1] == var_list[k]]
# 
# 
# death_low = len(group_low) - np.count_nonzero(group_low, axis=0)
# death_mid = len(group_mid) - np.count_nonzero(group_mid, axis=0)
# death_high = len(group_high) - np.count_nonzero(group_high, axis=0)
# =============================================================================


####################
# Plots
####################


# Plot 1: plot of random walk of the "average firm" per group

plot_matrix = np.matrix.transpose(result_matrix)

plt.figure(dpi=150)
for i in range(4):
    plt.plot(plot_matrix[:,i], label="Firm #{}".format(i+1))
plt.xlabel("Period number")
plt.ylabel("Wealth")
plt.title("Model 3 - Random walk of average firm for every group")
plt.legend(loc=4,prop={'size':10})
plt.show()


# =============================================================================
# # Plot 2: plot of the number of firms that died per group
# 
# plt.figure(dpi=150)
# 
# plt.plot(death_low, label="Firm #{}".format(1))
# plt.plot(death_mid, label="Firm #{}".format(2))
# plt.plot(death_high, label="Firm #{}".format(3))
# 
# plt.xlabel("Period number")
# plt.ylabel("Number of deaths")
# plt.title("Model 3 - Deaths over time from a total of {} firms per group".format(int(n/3)))
# plt.legend(loc=4,prop={'size':10})
# plt.show()
# =============================================================================







