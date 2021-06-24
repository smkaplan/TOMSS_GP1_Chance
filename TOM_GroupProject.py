# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 11:19:01 2021

@author: Robert Janjic
"""

import numpy as np
import matplotlib.pyplot as plt


n = 3*pow(10,3)       # number of agents (has to be divisible by 3 bc we have 3 groups)
t = 50                # number of periods
init_w = 1            # the initial wealth of firms (same for all)

var_low = 0.1       # variance of normal distribution for every group
var_mid = 0.3
var_high = 0.5

death_thresh = 0    # when wealth reaches this level, the firm dies

w = np.zeros((n, t))
w[:,0] = init_w


for i in range(n):
    for j in range(1, t):
        if w[i,j-1] <= death_thresh:
            continue
        else:
            if i%3 == 0:
                w[i,j] = w[i,j-1] + np.random.normal(0, var_low)
            elif i%3 == 1:
                w[i,j] = w[i,j-1] + np.random.normal(0, var_mid)
            else:
                w[i,j] = w[i,j-1] + np.random.normal(0, var_high)
            
            if w[i,j] <= death_thresh:
                w[i,j] = death_thresh

group_low = w[0]
group_mid = w[1]
group_high = w[2]

for i in range(3, len(w), 3):
    group_low = np.vstack((group_low, w[i]))
for i in range(4, len(w), 3):
    group_mid = np.vstack((group_mid, w[i]))
for i in range(5, len(w), 3):
    group_high = np.vstack((group_high, w[i]))

mean_low = np.mean(group_low, axis=0)
mean_mid = np.mean(group_mid, axis=0)
mean_high = np.mean(group_high, axis=0)

result_matrix = np.vstack((mean_low, mean_mid, mean_high))


# Plot of random walk of the "average firm" per group

plot_matrix = np.matrix.transpose(result_matrix)

plt.figure(dpi=150)
for i in range(3):
    plt.plot(plot_matrix[:,i], label="Firm #{}".format(i+1))
plt.xlabel("Period number")
plt.ylabel("Wealth")
plt.title("Random walk of average firm for every group")
plt.legend(loc=4,prop={'size':10})
plt.show()


# Plot of the number of firms that died per group

plt.figure(dpi=150)

death_low = len(group_low) - np.count_nonzero(group_low, axis=0)
plt.plot(death_low, label="Firm #{}".format(1))

death_mid = len(group_mid) - np.count_nonzero(group_mid, axis=0)
plt.plot(death_mid, label="Firm #{}".format(2))

death_high = len(group_high) - np.count_nonzero(group_high, axis=0)
plt.plot(death_high, label="Firm #{}".format(3))

plt.xlabel("Period number")
plt.ylabel("Number of deaths")
plt.title("Deaths over time from a total of {} firms per group".format(int(n/3)))
plt.legend(loc=4,prop={'size':10})
plt.show()







