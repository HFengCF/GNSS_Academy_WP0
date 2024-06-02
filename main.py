#!/usr/bin/env python39

# Author: Hao Feng Chen Fu

import sys, os
import numpy as np
import pandas as pd


def read_fields_file(path_name):
    dict = {}
    with open(path_name, 'r') as f:
        # Read file
        lines = f.readlines()
        
        for line in lines:
            if "#" in line:
                line_splited = line.replace("#", "").split()
                number_fields = len(line_splited)
                
                for i in range(1, number_fields):
                    dict[line_splited[i]] = []
    return dict

def fulfill_dict_fields(dict, path_name):
    with open(path_name, 'r') as f:
        # Read file
        lines = f.readlines()
        
        for line in lines:
            if "#" not in line:
                line_splited = line.split()
                
    return dict
 




if __name__ == "__main__":
   path_name = f"C:/Users/fengc/OneDrive/Documentos/WP0_RCVR_ANALYSIS/SCEN/SCEN_TLSA00615-GPSL1-SPP/OUT/LOS/TLSA00615_LosInfo_5s.dat"
   read_fields_file(path_name)