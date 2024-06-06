#!/usr/bin/env python39

# Author: Hao Feng Chen Fu

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import math
from search_file import read_fields_file, fill_data_fields

class POS_Charts:
    def __init__(self, df) -> None:
        self.dataframe = df
        self.dataframe['Hour'] = self.dataframe['SOD']/(3600)

        self.min_hour = min(self.dataframe['Hour'])
        self.max_hour = max(self.dataframe['Hour'])

    def get_dataframe(self):
        return self.dataframe
    
    def set_dataframe(self, df):
        self.dataframe = df

    def plot_linearplot(self, x_column_name, x_column_label, y_column_label, title_plot = "Default_Title", output_file_name = 'Output' , **kwargs):
        plt.rcParams["image.cmap"] = "gnuplot"
        # Change color set used: https://matplotlib.org/stable/gallery/color/colormap_reference.html
        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.Paired.colors)
        plt.figure(figsize=(10,6))

        for key, value in kwargs.items():
            plt.plot(self.dataframe[x_column_name], self.dataframe[value], label = value)

        title = title_plot + " from TLSA on Year {:n} DoY {:3n}".format(self.dataframe['YEAR'].iloc[0], self.dataframe['DOY'].iloc[0])

        plt.xlabel(x_column_label) 
        plt.ylabel(y_column_label) 
        plt.title(title) 

        plt.xlim(left = self.min_hour, right = self.max_hour)
        
        plt.legend()

        # plt.show()
        plt.savefig(output_file_name+'.png')
        



    def plot_scatterplot_POS(self, x_column_name, y_column_name, color_bar_column_name, y_div = 1,default_x_ticks =  False, default_y_ticks = False, title_plot = "Default_Title", x_label_name = None, y_label_name = None, color_bar_label_name = None,  output_file_name = 'Output'):
        dataframe = self.dataframe[[x_column_name, y_column_name, color_bar_column_name, 'DOY', 'YEAR']]
        dataframe[y_column_name] = dataframe[y_column_name]/y_div

        plt.figure(figsize=(10,6))

        if default_x_ticks == False:
            x_max_value = math.ceil(max(dataframe[x_column_name].values))
            plt.xlim(left = -2.5, right = 3)
            plt.xticks(ticks = range(-3, 3))

        if default_y_ticks == False:
            plt.ylim(bottom = -3, top = 5)
            plt.yticks(ticks = range(-3, 5))

        # Formats: https://www.w3schools.com/python/ref_string_format.asp
        title = title_plot + " from TLSA on Year {:n} DoY {:3n}".format(dataframe['YEAR'].iloc[0], dataframe['DOY'].iloc[0])

        plt.title(title)
        plt.xlabel(xlabel = x_label_name)
        plt.ylabel(ylabel = y_label_name)

        plt.grid(visible = True, axis = 'both', linestyle = '--', linewidth = 1, alpha = 0.4)
        plot = plt.scatter(x = dataframe[x_column_name].values, y = dataframe[y_column_name].values, c = dataframe[color_bar_column_name].values, cmap='gnuplot', marker = 's', s = 1)
        cbar = plt.colorbar(plot)
        cbar.set_label(color_bar_label_name)

        # plt.show()
        plt.savefig(output_file_name+'.png')

if __name__ == "__main__":
    path_name = f"C:/Users/fengc/OneDrive/Documentos/WP0_RCVR_ANALYSIS/SCEN/SCEN_TLSA00615-GPSL1-SPP/OUT/POS/TLSA00615_PosInfo_5s.dat"
    dict = read_fields_file(path_name)
    POS_graph = POS_Charts(fill_data_fields(dict, path_name))


    # Filling data
    dataframe = POS_graph.get_dataframe()
    dataframe['HPE'] = (dataframe['EPE[m]']**2 + dataframe['NPE[m]']**2)**0.5
    dataframe['VPE'] = abs(dataframe['UPE[m]'])
    POS_graph.set_dataframe(df = dataframe)

    POS_graph.plot_linearplot(x_column_name = 'Hour', x_column_label = 'Hour of DoY', y_column_label = 'Number of Satellites', title_plot = "Number of Satellites in PVT vs Time", output_file_name = 'POS_SATS_vs_TIME_TLSA_D006Y15', y_column_name = 'NSATS')

    POS_graph.plot_linearplot(x_column_name = 'Hour', x_column_label = 'Hour of DoY', y_column_label = 'DOP', title_plot = "Dilution of Precision (DOP)", output_file_name = 'POS_DOP_vs_TIME_TLSA_D006Y15', y_column_1 = 'GDOP', y_column_2 = 'PDOP', y_column_3 = 'TDOP')

    POS_graph.plot_linearplot(x_column_name = 'Hour', x_column_label = 'Hour of DoY', y_column_label = 'DOP', title_plot = "Dilution of Precision (DOP)", output_file_name = 'POS_HVDOP_vs_TIME_TLSA_D006Y15', y_column_1 = 'HDOP', y_column_2 = 'VDOP', y_column_3 = 'NSATS')

    POS_graph.plot_linearplot(x_column_name = 'Hour', x_column_label = 'Hour of DoY', y_column_label = 'ENU_PM[m]', title_plot = "ENU Position Error", output_file_name = 'POS_ENU_PE_vs_TIME_TLSA_D006Y15', y_column_1 = 'UPE[m]', y_column_2 = 'EPE[m]', y_column_3 = 'NPE[m]')
    
    POS_graph.plot_linearplot(x_column_name = 'Hour', x_column_label = 'Hour of DoY', y_column_label = 'H/VPE[m]', title_plot = "HPE-VPE Position Error", output_file_name = 'POS_HVPE_vs_TIME_TLSA_D006Y15', y_column_1 = 'VPE', y_column_2 = 'HPE')
   
    # T6.6 EPE vs. NPE plot
    POS_graph.plot_scatterplot_POS(x_column_name = 'EPE[m]', y_column_name = 'NPE[m]', color_bar_column_name = 'HDOP', y_div = 1, \
                           default_x_ticks = False, default_y_ticks = True, title_plot = "EPE vs NPE", \
                           x_label_name = 'EPE[m]', y_label_name = 'NPE[m]', color_bar_label_name = 'HDOP', \
                           output_file_name = 'POS_NPE_vs_EPE_TLSA_D006Y15'
                           )