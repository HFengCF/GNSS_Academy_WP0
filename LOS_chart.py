#!/usr/bin/env python39

# Author: Hao Feng Chen Fu

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import math
from search_file import read_fields_file, fill_data_fields

class LOS_Charts:
    def __init__(self, df) -> None:
        self.dataframe = df
        self.dataframe['Hour'] = self.dataframe['SOD']/(3600)

    def get_dataframe(self):
        return self.dataframe
    
    def set_dataframe(self, df):
        self.dataframe = df

    def plot_scatterplot(self, x_column_name, y_column_name, color_bar_column_name, y_div = 1, default_x_ticks =  False, default_y_ticks = False, title_plot = "Default_Title", x_label_name = None, y_label_name = None, color_bar_label_name = None):
        dataframe = self.dataframe[[x_column_name, y_column_name, color_bar_column_name, 'DOY', 'YEAR']]
        if y_div != 1:
            dataframe[y_column_name] = dataframe[y_column_name]/y_div

        plt.figure(figsize=(18,12))

        if default_x_ticks == False:
            x_max_value = math.ceil(max(dataframe[x_column_name].values))
            plt.xlim(left = 0, right =  x_max_value)
            plt.xticks(ticks = range(1, x_max_value))

        if default_y_ticks == False:
            plt.ylim(bottom = 0, top = (int(max(dataframe[y_column_name].values))+1) )
            plt.yticks(ticks = sorted(dataframe[y_column_name].unique()))

        # Formats: https://www.w3schools.com/python/ref_string_format.asp
        title = title_plot + " from TLSA on Year {:n} DoY {:3n}".format(dataframe['YEAR'].iloc[0], dataframe['DOY'].iloc[0])

        plt.title(title)
        plt.xlabel(xlabel = x_label_name)
        plt.ylabel(ylabel = y_label_name)

        plt.grid(visible = True, axis = 'both', linestyle = '--', linewidth = 1, alpha = 0.4)
        plot = plt.scatter(x = dataframe[x_column_name].values, y = dataframe[y_column_name].values, c = dataframe[color_bar_column_name].values, cmap='gnuplot', marker = 's', s = 1)
        cbar = plt.colorbar(plot)
        cbar.set_label(color_bar_label_name)

        plt.show()

    def plot_scatterplot_in_map(self, x_pos_column, y_pos_column, z_pos_column, color_bar_column_name, title_plot = "Default title"):
        dataframe = self.dataframe[['DOY', 'YEAR', x_pos_column, y_pos_column, z_pos_column, color_bar_column_name]]

        dataframe['LON'] = np.degrees(np.arctan2(dataframe['SAT-Y[m]'], dataframe['SAT-X[m]']))
        dataframe['LAT'] = np.degrees(np.arcsin(dataframe['SAT-Z[m]'] / np.sqrt(dataframe['SAT-X[m]']**2 + dataframe['SAT-Y[m]']**2 + dataframe['SAT-Z[m]']**2)))
        plt.figure(figsize=(18, 12))

        title = title_plot + " from TLSA on Year {:n} DoY {:3n}".format(dataframe['YEAR'].iloc[0], dataframe['DOY'].iloc[0])

        # Source: https://semba-blog.netlify.app/07/04/2020/mapping-with-cartopy-in-python/
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.coastlines()
        # ax.set_global()
        ax.set_extent([-135, 135, -35, 90], crs=ccrs.PlateCarree())         # Set map size
        ax.gridlines(draw_labels=True, xlocs=np.arange(-135, 135, 5), ylocs=np.arange(-35, 90, 5))

        plt.title(title)

        plt.grid(visible = True, axis = 'both', linestyle = '--', linewidth = 1, alpha = 0.4)
        plot = plt.scatter(x = dataframe['LON'].values, y = dataframe['LAT'], c = dataframe[color_bar_column_name].values, cmap='gnuplot', s = 1)
        cbar = plt.colorbar(plot, shrink = 0.75)
        cbar.set_label('Elevation [deg]')

        plt.show()

    def plot_multiple_scatterplot(self, x_column_name, y_column_name, filter_by, y_div = 1, default_x_ticks =  False, default_y_ticks = False, title_plot = "Default_Title", x_label_name = None, y_label_name = None):
        dataframe = self.dataframe[[x_column_name, y_column_name, filter_by, 'DOY', 'YEAR']]
        if y_div != 1:
            dataframe[y_column_name] = dataframe[y_column_name]/y_div

        dataframe[[filter_by]] = dataframe[[filter_by]].astype(str)

        list_unique_values = sorted(list(dataframe[filter_by].unique()))

        for i in list_unique_values:
            plt.figure(figsize=(18,12))
            df_aux = dataframe[dataframe[filter_by].str.contains(i)]

            df_aux[[filter_by]] = df_aux[[filter_by]].astype(float)

            if default_x_ticks == False:
                x_max_value = math.ceil(max(dataframe[x_column_name].values))
                plt.xlim(left = 0, right =  x_max_value)
                plt.xticks(ticks = range(1, x_max_value))

            if default_y_ticks == False:
                plt.ylim(bottom = 0, top = (int(max(dataframe[y_column_name].values))+1) )
                plt.yticks(ticks = sorted(dataframe[y_column_name].unique()))

            # Formats: https://www.w3schools.com/python/ref_string_format.asp
            title = title_plot + " PRN {} from TLSA on Year {:n} DoY {:3n}".format(i, dataframe['YEAR'].iloc[0], dataframe['DOY'].iloc[0])
            plt.title(title)
            plt.xlabel(xlabel = x_label_name)
            plt.ylabel(ylabel = y_label_name)

            plt.grid(visible = True, axis = 'both', linestyle = '--', linewidth = 1, alpha = 0.4)
            plot = plt.scatter(x = dataframe[x_column_name].values, y = dataframe[y_column_name].values, marker = 's', s = 1)
            plt.show()

    def plot_multiple_plot(self, x_column_name, y_column_name, filter_by, y_div = 1, default_x_ticks =  False, default_y_ticks = False, title_plot = "Default_Title", x_label_name = None, y_label_name = None):
        dataframe = self.dataframe[[x_column_name, y_column_name, filter_by, 'DOY', 'YEAR']]
        if y_div != 1:
            dataframe[y_column_name] = dataframe[y_column_name]/y_div

        dataframe[[filter_by]] = dataframe[[filter_by]].astype(str)

        list_unique_values = sorted(list(dataframe[filter_by].unique()))

        for i in list_unique_values:
            plt.figure(figsize=(18,12))
            df_aux = dataframe[dataframe[filter_by].str.contains(i), x_column_name]

            df_aux[[filter_by]] = df_aux[[filter_by]].astype(float)

            if default_x_ticks == False:
                x_max_value = math.ceil(max(dataframe[x_column_name].values))
                plt.xlim(left = 0, right =  x_max_value)
                plt.xticks(ticks = range(1, x_max_value))

            if default_y_ticks == False:
                plt.ylim(bottom = 0, top = (int(max(dataframe[y_column_name].values))+1) )
                plt.yticks(ticks = sorted(dataframe[y_column_name].unique()))

            # Formats: https://www.w3schools.com/python/ref_string_format.asp
            title = title_plot + " PRN {} from TLSA on Year {:n} DoY {:3n}".format(i, dataframe['YEAR'].iloc[0], dataframe['DOY'].iloc[0])
            plt.title(title)
            plt.xlabel(xlabel = x_label_name)
            plt.ylabel(ylabel = y_label_name)

            plt.grid(visible = True, axis = 'both', linestyle = '--', linewidth = 1, alpha = 0.4)
            plot = plt.scatter(x = df_aux[x_column_name].values, y = df_aux[y_column_name].values, marker = 's', s = 1)
            plt.show()


if __name__ == "__main__":
    path_name = f"C:/Users/fengc/OneDrive/Documentos/WP0_RCVR_ANALYSIS/SCEN/SCEN_TLSA00615-GPSL1-SPP/OUT/LOS/TLSA00615_LosInfo_5s.dat"
    dict = read_fields_file(path_name)
    LOS_graph = LOS_Charts(fill_data_fields(dict, path_name))

    # Filling data
    dataframe = LOS_graph.get_dataframe()
    dataframe['ABS_VEL'] = ((dataframe['VEL-X[m/s]']/1000)**2 + (dataframe['VEL-Y[m/s]']/1000)**2 + (dataframe['VEL-Z[m/s]']/1000)**2)**0.5
    dataframe['CLK_P1[km]'] = dataframe['SV-CLK[m]']/1000 - dataframe['TGD[m]'] + dataframe['DTR[m]']
    dataframe['ELEV_radians'] = dataframe['ELEV']*(math.pi/180)
    dataframe['ZTD'] = dataframe['TROPO[m]'] / (1.001 / (0.002001 + np.sin(dataframe['ELEV_radians'])**2 )**0.5 )
    LOS_graph.set_dataframe(df = dataframe)

    # ------------------------------------------------- T2 ----------------------------------------------------------------------------

    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'PRN', color_bar_column_name = 'ELEV', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = False, title_plot = "Satellite Visibility", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'GPS-PRN', color_bar_label_name = 'Elevation [deg]'
    #                        )
    
    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'RANGE[m]', color_bar_column_name = 'ELEV', y_div = 1000, \
    #                        default_x_ticks = True, default_y_ticks = True, title_plot = "Satellite Geometical Range", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'RANGE[km]', color_bar_label_name = 'Elevation [deg]'
    #                        )
    
    # LOS_graph.plot_scatterplot_in_map(x_pos_column = 'SAT-X[m]', y_pos_column = 'SAT-Y[m]', z_pos_column = 'SAT-Z[m]', color_bar_column_name = 'ELEV', \
    #                               title_plot = 'Satellite Tracks during visibility periods', color_bar_label_name ='Elevation [deg]')
    
    # dataframe = LOS_graph.get_dataframe()
    # dataframe['ABS_VEL'] = ((dataframe['VEL-X[m/s]']/1000)**2 + (dataframe['VEL-Y[m/s]']/1000)**2 + (dataframe['VEL-Z[m/s]']/1000)**2)**0.5

    # LOS_graph.set_dataframe(df = dataframe)

    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'ABS_VEL', color_bar_column_name = 'ELEV', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Satellite Range Velocity", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'Absolute Velocity [km/s]', color_bar_label_name = 'Elevation [deg]'
    #                        )
    
    # T2.5 NAV Satellite Clock in process
    # LOS_graph.plot_multiple_scatterplot(x_column_name = 'Hour', y_column_name = 'SV-CLK[m]', filter_by = 'PRN', default_x_ticks = False, default_y_ticks = False, title_plot = "NAV CLK", x_label_name = None, y_label_name = None)


    # T2.6 Satellite Clock still in process
    LOS_graph.plot_multiple_scatterplot(x_column_name = 'Hour', y_column_name = 'SV-CLK[m]', filter_by = 'PRN', default_x_ticks = False, default_y_ticks = True, title_plot = "NAV CLK", x_label_name = None, y_label_name = None)

    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'CLK_P1[km]', color_bar_column_name = 'PRN', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Satellite CLK + DTR - TGD", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'CLK[km]', color_bar_label_name = 'GPS-PRN'
    #                        )


    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'TGD[m]', color_bar_column_name = 'PRN', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Satellite TGD (Total Group Delay)", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'TGD[m]', color_bar_label_name = 'GPS-PRN'
    #                        )

    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'DTR[m]', color_bar_column_name = 'ELEV', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Satellite DTR (Clock Relativistic Effect)", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'DTR[m]', color_bar_label_name = 'Elevation [deg]'
    #                        )
    
    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'STEC[m]', color_bar_column_name = 'ELEV', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Ionispheric Klobuchar Delay (STEC)", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'STEC[m]', color_bar_label_name = 'Elevation [deg]'
    #                        )
    
    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'PRN', color_bar_column_name = 'STEC[m]', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Satellite Visibility vs STEC", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'GPS-PRN', color_bar_label_name = 'STEC[m]'
    #                        )

    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'VTEC[m]', color_bar_column_name = 'ELEV', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Ionosppheric Klobuchar Delays (VTEC)", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'VTEC[m]', color_bar_label_name = 'ELEV'
    #                        )
    
    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'PRN', color_bar_column_name = 'VTEC[m]', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Satellite Visibility vs VTEC", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'GPS-PRN', color_bar_label_name = 'VTEC[m]'
    #                        )
    
    # Zenith GOOD
    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'ZTD', color_bar_column_name = 'ELEV', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Zenith Tropospheric Delays (ZTD)", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'ZTD', color_bar_label_name = 'Elevation [deg]'
    #                        )
    
    # T5.1 Pseudo Ranges






    # T5.3
    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'TOF[ms]', color_bar_column_name = 'ELEV', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Time of Flight (ToF)", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'TOF[ms]', color_bar_label_name = 'Elevation [deg]'
    #                        )