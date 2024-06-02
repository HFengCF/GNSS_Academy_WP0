#!/usr/bin/env python39

# Author: Hao Feng Chen Fu

import sys, os
import numpy as np
import pandas as pd
import matplotlib

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
 
def plot_sat_visibility(dataframe):
    pass




if __name__ == "__main__":
   path_name = f"C:/Users/fengc/OneDrive/Documentos/WP0_RCVR_ANALYSIS/SCEN/SCEN_TLSA00615-GPSL1-SPP/OUT/LOS/TLSA00615_LosInfo_5s.dat"
   dict = read_fields_file(path_name)
   print(dict)
   dataframe = fulfill_dict_fields(dict, path_name)
   print(dataframe)

   dataframe.plot.scatter(x ="SOD", y="PRN", c="ELEV")

   print("Hello world")
   