#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 15:36:55 2018

@author: Stephan R. Hlohowskyj

"""

###############################################################################
################# import dependent packages for analysis ######################
###############################################################################

import os
import glob
import random
import decimal
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

###############################################################################
###### Define some functions needed to calculate the sedimentation rates ######
###############################################################################

#set collection date of the core (i.e., final trip to the lake) May 2016
startdate = 2016.5

#calculate 10000 sediment rates from the 1 sigma ranges of the 210Pb dates in Conroy et al., 2014
def MonteCarloSed():
    sedrate = float(decimal.Decimal(random.randrange(118,241))/10000)
    return sedrate

#read the core depths from a text file
def CoreReader(y, FileName):
    a1=[]
    with open(FileName) as f:
        for line in f:
            data = line.split()
            a1.append(float(data[0]))
    return a1[y]

#read the Mo/Ti values from a text file
def MoReader(m, FileName):
    a2=[]
    with open(FileName) as f:
        for line in f:
            data = line.split()
            a2.append(float(data[0]))
    return a2[m]


#calculate the age dates based on sediment rate
def sedplot(x1, x2, x3):
    test = CoreReader(x1, x3) / sedresultnorm[x2]
    agedate = startdate - test
    return agedate

#count the number of years that fall within ± 'a defined error' of El Nino CDF years
def computeyearprob(list1, l, r):
    c = 0
    for x in list1:
        if x >= l and x <= r:
            c += 1
    return c

#find the closest value to a CDF ENSO year
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

#Define the scipt to capture all ages related to Mo/Ti values above crustal
def ENSO_proxy():
    ElNino = [i for i, v in enumerate(Mo_results) if v > 0]
    return ElNino

#define a script to create a new array with all possible ages for each Mo value
def ENSO_proxy_stats(reps):
    k=0
    times1=0
    times2=0
    while k < reps:
        ENSOstats=[]
        while times1 < len(newmodel):
            ENSOstats.append(newmodel[times1][MoNino[times2]])
            times1 += 1
        k += 1
        times2 += 1
        times1 = 0
        ENSOstats2.append(ENSOstats)

###############################################################################
######### begin to call functions and construct age models, data, etc #########
###############################################################################

#Define needed arrays
sedresult=[]
sedresultnorm=[]
modelrange=[]
newmodel=[]
Mo_results=[]
Fe_results=[]

#call the Monte carlo function
t = 0
while t < 10000:
    sedresult.append(MonteCarloSed()) # / 1000)
    t+=1

#sample the 1000 random rates with a normal distribution
sedresultnorm = np.random.normal(0.168, 0.033, 10000)

#Create new arrays that have geochemical data and an assigned sedimentation rate
z1=0
z3=0
for x in range(0,10000):
    z = 0
    a3=[]
    a4=[]
    while z < 27:
        a4.append(sedplot(z,z3,'core_16_composite_depth.txt'))
        z+=1
    z1+=1
    z3+=1
    newmodel.append(a4)

n = 0
depths=[]
while n < 27:
    Mo_results.append(MoReader(n, 'core_16_composite_Mo.txt'))
    Fe_results.append(MoReader(n, 'core_16_composite_Fe.txt'))
    depths.append(CoreReader(n, 'core_16_composite_depth.txt'))
    n+=1

'''
#Show plots of age models (use for debugging)
z3=0
while z3 < 10000:
    plt.plot(depths, newmodel[z3], 'o', color='black', alpha=0.004)
    z3+=1

plt.ylabel('year')
plt.xlabel('depth(cm)')
plt.show()

#Show sedimentation rates (use for debugging)
plt.hist(sedresultnorm, color='blue', edgecolor='black', bins=40)
plt.ylabel('frequency')
plt.xlabel('sed rate (cm/yr)')
plt.show()

#give values (use for debugging)
print("standard deviation:", np.std(sedresultnorm))
print("mean value:", np.mean(sedresultnorm))
print(stats.mode(sedresultnorm))
'''

#create new arrays for analysis of age model, geochemical data, and ENSO events
ENSOstats2 = []
MoNino = []
ENSO_mean=[]
ENSO_std=[]

MoNino = ENSO_proxy()
ENSO_proxy_stats(len(MoNino))

l=0
while l < len(MoNino):
    ENSO_mean.append(np.median(ENSOstats2[l]))
    ENSO_std.append(np.std(ENSOstats2[l]))
    l+=1

#set variables to test against data set, data derived from Charles Darwin Foundation SST dataset
cdf = [0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,1,0,0,1,0,1,0,1,0]
event = 0
counter = [7, 14, 15, 16, 17, 19, 20, 21, 23]
comparemean = 0
CDFplot=[]
CDFtropical=[2009, 2007, 1998, 1992, 1987, 1984, 1983, 1977, 1973, 1969, 1966]
test = []

a = 0
yearcalc = []
ENSOhits = []
prob = []
plotENSO = []
lowerwidth = []
upperwidth = []

#create a probaility of a trace metal enrichment being aligned with an ENSO event

while event < 27 :
    compareENSO=[]
    t = 0
    while t < 10000 :
        compareENSO.append(newmodel[t][event])
        t += 1
    #find the median year from 10000 ages which could correspond to first possible event
    comparemean=np.median(compareENSO) #fist attempts used the mean year, median was found to be a better value
    CDFplot.append(comparemean)
    yearcalc = find_nearest(CDFtropical, CDFplot[event])
    plotENSO.append(yearcalc)
    quartile1 = np.percentile(compareENSO, 25)
    quartile3 = np.percentile(compareENSO, 75)
    lowerbound = CDFplot[event]-quartile1 #calculate number of years from median point)
    upperbound = quartile3-CDFplot[event] #calculate number of years from median point)
    ENSOhits = computeyearprob(compareENSO, yearcalc - lowerbound, yearcalc + upperbound)
    prob.append(ENSOhits / 5000)
    print(ENSOhits)
    event += 1

###############################################################################
########### begin create plots for age models and geochemical data ############
###############################################################################

#create plot for age model probability of an ENSO event
plt.plot(CDFplot, prob, marker='x', color='black')
#plt.ylim(0, 1.0)
#plt.xlabel('mean year')
#plt.ylabel('CDF measured')
#plt.savefig('CDFplot.png', dpi=300)
print(prob)
plt.show()

alpha01=[]
alpha05=[]
others=[]
Fe_alpha01=[]
Fe_alpha05=[]
Fe_others=[]
x = 0
vertical_line = []

#Create Mo lists for box and whisker plots
while x < len(prob) :
    if prob[x] > 0.99 :
        alpha01.append(Mo_results[x])
        vertical_line.append(ENSO_mean[x])
    if prob[x] > 0.95 :
        alpha05.append(Mo_results[x])
    if prob[x] < 0.99 :
        others.append(Mo_results[x])
        vertical_line.append(0)
    x+=1

alldata = [others, alpha01]
x=0

#Create Fe lists for box and whisker plots
while x < len(prob) :
    if prob[x] > 0.99 :
        Fe_alpha01.append(Fe_results[x])
    if prob[x] > 0.95 :
        Fe_alpha05.append(Fe_results[x])
    if prob[x] < 0.99 :
        Fe_others.append(Fe_results[x])
    x+=1

all_Fe_data = [Fe_others, Fe_alpha01]

#Use matlab plot to create plots for Mo and Fe data box and whiskers and age model
plt.boxplot(alldata, labels=['Neutral + La Niña', 'El Niño'])
plt.ylim(0, 20)
plt.ylabel('Mo/Ti')
#plt.savefig('alpha001_mo.png', dpi=300)
plt.show()

plt.boxplot(all_Fe_data, labels=['Neutral + La Niña', 'El Niño'])
#plt.ylim(0, 100)
plt.ylabel('Fe/Ti')
#plt.savefig('alpha001_Fe.png', dpi=300)
plt.show()

z4=0
while z4 < 10000:
    plt.plot(newmodel[z4], Mo_results, color='black', alpha=0.006)
    plt.xlim(1965)
    z4+=1

u = 0
while u < 27:
    plt.axvline(x=vertical_line[u], c='red', alpha=0.7, lw=2)
    u+=1

plt.plot(ENSO_mean, Mo_results, marker='o', color='white', fillstyle='full', markeredgecolor='black',markeredgewidth=0.5)
plt.xlabel('year')
plt.ylabel('Mo/Ti')
ax = plt.axes()
ax.minorticks_on()
ax.tick_params(which='both', direction='in')
#ax.grid(which='major')
plt.savefig('newmodel_Mo.png', dpi=300)
plt.show()

z4=0
while z4 < 10000:
    plt.plot(newmodel[z4], Fe_results, color='black', alpha=0.006)
    plt.xlim(1965)
    z4+=1

u = 0
while u < 27:
    plt.axvline(x=vertical_line[u], c='red', alpha=0.7, lw=2)
    u+=1

plt.plot(ENSO_mean, Fe_results, marker='o', color='white', fillstyle='full', markeredgecolor='black',markeredgewidth=0.5)
plt.xlabel('year')
plt.ylabel('Fe/Ti')
plt.savefig('newmodel_Fe.png', dpi=300)
plt.show()

###############################################################################
####### Output text files from analysis for use in other applications #########
###############################################################################

#saving output files from analysis
save_path = os.getcwd()
ifile = "/testing_Mo.txt"

with open(save_path + ifile, 'w') as outfile:
    outfile.write("Mo_value Mean_year\n")
    for i in range(len(Mo_results)):
        outfile.write("%.1f %.1f\n" % (Mo_results[i], ENSO_mean[i]))

ifile = "/testing_Fo.txt"

with open(save_path + ifile, 'w') as outfile:
    outfile.write("Fe_value Mean_year\n")
    for i in range(len(Mo_results)):
        outfile.write("%.1f %.1f\n" % (Fe_results[i], ENSO_mean[i]))
