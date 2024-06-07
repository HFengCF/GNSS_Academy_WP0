import sys, os
import pandas as pd
import numpy as np
import math

from POS_chart import POS_Charts
from LOS_chart import LOS_Charts

import features
import constants as cons

from search_file import read_fields_file, fill_data_fields

def main():
    pd.options.mode.chained_assignment = None
    # Scen_path = sys.argv[1]
    Scen_path = f'C:/Users/fengc/OneDrive/Documentos/WP0_RCVR_ANALYSIS/SCEN/SCEN_TLSA00615-GPSL1-SPP'
    # folder_output = Scen_path + '/OUTPUT_SCEN_TLSA00615-GPSL1-SPP'

    # print('Path: ', folder_output)
    # if not os.path.exists(folder_output):
    #     os.makedirs(folder_output)

    # if not os.path.exists(folder_output+'/SubPlots'):
    #     os.makedirs(folder_output+'/SubPlots')

    generate_LOS_figures(Scen_path)

    # generate_POS_figures(Scen_path+cons.POS_path)



def generate_LOS_figures(path_out = None):
    # path_name = f"C:/Users/fengc/OneDrive/Documentos/WP0_RCVR_ANALYSIS/SCEN/SCEN_TLSA00615-GPSL1-SPP/OUT/LOS/TLSA00615_LosInfo_5s.dat"
    path_name = path_out + cons.LOS_path
    folder_output = path_out + '/OUTPUT/LOS/'

    if not os.path.exists(folder_output):
        print('Create Folder: ', folder_output)
        os.makedirs(folder_output)

    if not os.path.exists(folder_output+'/SubPlots'):
        print('Create SubFolder: ', folder_output)
        os.makedirs(folder_output+'/SubPlots')

    print('----------------------------------------')
    print('LOS Charts generation...')
    print('----------------------------------------')

    dict = read_fields_file(path_name)
    LOS_graph = LOS_Charts(fill_data_fields(dict, path_name), output_path = folder_output)

    """ ----------------------------------------- Filling data ----------------------------------------- """
    dataframe = LOS_graph.get_dataframe()
    # T2.4
    dataframe['ABS_VEL[m]'] = ((dataframe['VEL-X[m/s]'])**2 + (dataframe['VEL-Y[m/s]'])**2 + (dataframe['VEL-Z[m/s]'])**2)**0.5
    dataframe['ABS_VEL[km]'] = dataframe['ABS_VEL[m]']/1000

    # T2.6
    dataframe['CLK_P1[km]'] = dataframe['SV-CLK[m]']/1000 - dataframe['TGD[m]']/1000 + dataframe['DTR[m]']/1000

    # T4.2
    dataframe['ELEV_radians'] = dataframe['ELEV']*(math.pi/180)
    dataframe['ZTD'] = dataframe['TROPO[m]'] / (1.001 / (0.002001 + np.sin(dataframe['ELEV_radians'])**2 )**0.5 )

    # T5.2 
    dataframe['Tau[ms]'] = dataframe['TROPO[m]']/cons.light_speed

    # T5.4
    dataframe['R_LOS[m]'] = (dataframe['SAT-X[m]']**2 + dataframe['SAT-Y[m]']**2 + dataframe['SAT-Z[m]']**2)**0.5 - (cons.x_pos_receiver**2 + cons.y_pos_receiver**2 + cons.z_pos_receiver**2)**0.5
    dataframe['V_LOS[m]'] = dataframe['ABS_VEL[m]'] * ( dataframe['R_LOS[m]'] / abs(dataframe['R_LOS[m]']) )
    dataframe['F_Doppler'] = - ( dataframe['V_LOS[m]']/cons.light_speed ) * cons.frecuency_L1

    # T5.5
    dataframe['RES[km]'] = dataframe['MEAS[m]']/1000 - (dataframe['RANGE[m]']/1000 - dataframe['CLK_P1[km]'] + dataframe['STEC[m]']/1000 + dataframe['TROPO[m]']/1000)

    LOS_graph.set_dataframe(df = dataframe)
    """ ------------------------------------------------------------------------------------------------ """

    # for key, value in features.LOS_scatterplot_data.items():
    #     # If a put pos_args = value y got this error:     LOS_graph.plot_multiple_sub_scatterplot(*pos_args) TypeError: plot_multiple_sub_scatterplot() takes from 4 to 11 positional arguments but 12 were given
    #     pos_args = value
    #     LOS_graph.plot_scatterplot(*pos_args)
    
    # for key, value in features.LOS_scatterplot_map_data.items():
    #     pos_args = value
    #     LOS_graph.plot_scatterplot_in_map(*pos_args)

    for key, value in features.LOS_CLK_scatter_plots.items():
        pos_args = value
        LOS_graph.plot_multiple_sub_scatterplot(*pos_args)



def generate_POS_figures(path_name = None):
    # if path_name == None:
    #     print('No path has been provided for LOS data')
    #     exit()
    dict = read_fields_file(path_name)
    POS_graph = POS_Charts(fill_data_fields(dict, path_name))

    print('----------------------------------------')
    print('LOS Charts generation...')
    print('----------------------------------------')

    """ ----------------------------------------- Filling data ----------------------------------------- """
    dataframe = POS_graph.get_dataframe()
    dataframe['HPE'] = (dataframe['EPE[m]']**2 + dataframe['NPE[m]']**2)**0.5
    dataframe['VPE'] = abs(dataframe['UPE[m]'])
    POS_graph.set_dataframe(df = dataframe)
    """ ------------------------------------------------------------------------------------------------ """

    for key, value in features.POS_plots.items():
        pos_args = value[:5]
        kw_args = {}

        if len(value) > 5:
            extra_args = value[5:]
            for i, extra_arg in enumerate(extra_args):
                kw_args[f'kwarg{i+1}'] = extra_arg

        POS_graph.plot_linearplot(*pos_args, **kw_args)

    for key, value in features.POS_scatterplot.items():
        POS_graph.plot_scatterplot_POS(*value)


if __name__ == "__main__":
    main()