import pandas as pd
import os, sys

def read_fields_file(path_name) -> dict:
    fields = {}

    if os.path.exists(path_name) == False:
        print("The path doesn't exist,  please check it out : {}".format(path_name))
        sys.exit()

    with open(path_name, 'r') as f:
        # Read file
        lines = f.readlines()
        
        for line in lines:
            if "#" in line:
                line_splited = line.replace("#", "").split()
                number_fields = len(line_splited)
                
                for i in range(1, number_fields+1):
                    fields[line_splited[i-1]] = []
    return fields

def fill_data_fields(dict, path_name) -> pd.DataFrame:
    columns = list(dict.keys())     # Get columns names

    with open(path_name, 'r') as f:
        # Read file
        lines = f.readlines()
        
        for line in lines:
            if "#" not in line:
                line_splited = line.split()

                for i in range(1, len(line_splited)+1):
                    dict[columns[i-1]].append(float(line_splited[i-1]))


    return pd.DataFrame(dict)


if __name__ == "__main__":
    path_name = f"C:/Users/fengc/OneDrive/Documentos/WP0_RCVR_ANALYSIS/SCEN/SCEN_TLSA00615-GPSL1-SPP/OUT/LOS/TLSA00615_LosInfo_5s.dat"
    dict = read_fields_file(path_name)
    print(fill_data_fields(dict, path_name))
