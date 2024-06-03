#!/usr/bin/env python39

# Author: Hao Feng Chen Fu

import sys, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def read_fields_file(path_name):
    fields = {}
    with open(path_name, 'r') as f:
        # Read file
        lines = f.readlines()
        
        for line in lines:
            if "#" in line:
                line_splited = line.replace("#", "").split()
                number_fields = len(line_splited)
                
                for i in range(1, number_fields):
                    fields[line_splited[i-1]] = []
    return fields

def fulfill_dict_fields(dict, path_name):
    columns = list(dict.keys())     # Get columns names

    with open(path_name, 'r') as f:
        # Read file
        lines = f.readlines()
        
        for line in lines:
            if "#" not in line:
                line_splited = line.split()

                for i in range(1, len(line_splited)):
                    dict[columns[i-1]].append(float(line_splited[i-1]))

    # Create dataframe
    dataframe = pd.DataFrame(dict)

    dataframe[['DOY', 'YEAR', 'PRN']] = dataframe[['DOY', 'YEAR', 'PRN']].astype(int)

    return dataframe    
 
def plot_sat_visibility(df):
    dataframe = df[['SOD', 'PRN', 'ELEV']]
    dataframe['SOD'] = dataframe['SOD']/(3600)

    plt.figure()

    plt.xlim(left = 0, right =  24)
    plt.xticks(ticks = range(1, 24))

    plt.ylim(bottom = 0, top = (int(max(dataframe['PRN'].values))+1) )
    plt.yticks(ticks = sorted(dataframe['PRN'].unique()))

    plt.title('Satellite Visibility from TLSA on Year 2015 and DoY 006')
    plt.xlabel(xlabel = 'Hour of DoY 006')
    plt.ylabel(ylabel = 'GPS-PRN')

    plt.grid(visible = True, axis = 'both', linestyle = '--', linewidth = 1, alpha = 0.4)

    # Markers: https://matplotlib.org/stable/api/markers_api.html
    plot = plt.scatter(x = dataframe['SOD'].values, y = dataframe['PRN'].values, c = dataframe['ELEV'].values, cmap='gnuplot', marker = 's', s = 1,
                )
    cbar = plt.colorbar(plot)
    cbar.set_label('Elevation [deg]')

    plt.show()

def plot_geometrical_range(df):
    dataframe = df[['SOD', 'RANGE[m]', 'ELEV']]
    dataframe['SOD'] = dataframe['SOD']/(3600)
    dataframe['RANGE[m]'] = dataframe['RANGE[m]']/1000

    plt.figure()

    plt.xlim(left = 0, right =  24)
    plt.xticks(ticks = range(1, 24))

    # Lines commented because of high processing
    # plt.ylim(bottom = (int(min(dataframe['RANGE[m]'].values))-1000) , top = (int(max(dataframe['RANGE[m]'].values))+1000) )
    # plt.yticks(ticks = sorted(dataframe['RANGE[m]'].unique()))

    plt.title('Satellite Visibility from TLSA on Year 2015 and DoY 006')
    plt.xlabel(xlabel = 'Hour of DoY 006')
    plt.ylabel(ylabel = 'Range[km]')

    plt.grid(visible = True, axis = 'both', linestyle = '--', linewidth = 1, alpha = 0.4)

    # Markers: https://matplotlib.org/stable/api/markers_api.html
    plot = plt.scatter(x = dataframe['SOD'].values, y = dataframe['RANGE[m]'].values, c = dataframe['ELEV'].values, cmap='gnuplot', s = 1)
    cbar = plt.colorbar(plot)
    cbar.set_label('Elevation [deg]')

    plt.show()



if __name__ == "__main__":
    path_name = f"C:/Users/fengc/OneDrive/Documentos/WP0_RCVR_ANALYSIS/SCEN/SCEN_TLSA00615-GPSL1-SPP/OUT/LOS/TLSA00615_LosInfo_5s.dat"
    dict = read_fields_file(path_name)
    dataframe = fulfill_dict_fields(dict, path_name)
    print(dataframe)
    plot_sat_visibility(dataframe)
    plot_geometrical_range(dataframe)