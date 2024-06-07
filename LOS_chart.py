#!/usr/bin/env python39

# Author: Hao Feng Chen Fu

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import math
from search_file import read_fields_file, fill_data_fields

class LOS_Charts:
    def __init__(self, df, output_path = None) -> None:
        self.dataframe = df
        self.dataframe['Hour'] = self.dataframe['SOD']/(3600)
        self.dataframe[['DOY', 'YEAR']] = self.dataframe[['DOY', 'YEAR']].astype(int)
        if output_path is not None:
            self.output_path = output_path
        else:
            self.output_path = ""  

    def get_dataframe(self):
        return self.dataframe
    
    def set_dataframe(self, df):
        self.dataframe = df

    def plot_scatterplot(self, x_column_name, y_column_name, color_bar_column_name, y_div = 1, default_x_ticks =  False, default_y_ticks = False, title_plot = "Default_Title", x_label_name = None, y_label_name = None, color_bar_label_name = None, output_file_name = "Output"):
        dataframe = self.dataframe[[x_column_name, y_column_name, color_bar_column_name, 'DOY', 'YEAR']]

        print(title_plot+'...')

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
        title = title_plot + " from TLSA on Year {:n} DoY {}".format(dataframe['YEAR'].iloc[0], str(dataframe['DOY'].iloc[0]).zfill(3))

        plt.title(title)
        plt.xlabel(xlabel = x_label_name)
        plt.ylabel(ylabel = y_label_name)

        plt.grid(visible = True, axis = 'both', linestyle = '--', linewidth = 1, alpha = 0.4)
        plot = plt.scatter(x = dataframe[x_column_name].values, y = dataframe[y_column_name].values, c = dataframe[color_bar_column_name].values, cmap='gnuplot', marker = 's', s = 1)
        cbar = plt.colorbar(plot)
        cbar.set_label(color_bar_label_name)

        # plt.show()
        plt.savefig(self.output_path+output_file_name+'.png')
        plt.close()

    def plot_scatterplot_in_map(self, x_pos_column, y_pos_column, z_pos_column, color_bar_column_name, title_plot = "Default title", color_bar_label_name = None, output_file_name = "Output"):
        dataframe = self.dataframe[['DOY', 'YEAR', x_pos_column, y_pos_column, z_pos_column, color_bar_column_name]]

        print(title_plot+'...')

        dataframe['LON'] = np.degrees(np.arctan2(dataframe['SAT-Y[m]'], dataframe['SAT-X[m]']))
        dataframe['LAT'] = np.degrees(np.arcsin(dataframe['SAT-Z[m]'] / np.sqrt(dataframe['SAT-X[m]']**2 + dataframe['SAT-Y[m]']**2 + dataframe['SAT-Z[m]']**2)))
        plt.figure(figsize=(18, 12))

        title = title_plot + " from TLSA on Year {:n} DoY {}".format(dataframe['YEAR'].iloc[0], str(dataframe['DOY'].iloc[0]).zfill(3))

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
        cbar.set_label(color_bar_label_name)

        # plt.show()
        plt.savefig(self.output_path+output_file_name+'.png')
        plt.close()

    def plot_multiple_sub_scatterplot(self, x_column_name, y_column_name, filter_by, y_div = 1, default_x_ticks =  False, default_y_ticks = False, title_plot = "Default_Title", x_label_name = None, y_label_name = None, output_file_name = "Output"):
        dataframe = self.dataframe[[x_column_name, y_column_name, filter_by, 'DOY', 'YEAR']]

        print(title_plot+'...')

        if y_div != 1:
            dataframe[y_column_name] = dataframe[y_column_name]/y_div

        dataframe[[filter_by]] = dataframe[[filter_by]].astype(str)

        list_unique_values = sorted(list(dataframe[filter_by].unique()))

        for i in list_unique_values:
            print(title_plot+' '+filter_by+str(int(float(i)))+'...')
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
            title = title_plot + " PRN {} from TLSA on Year {:n} DoY {}".format(int(float(i)), dataframe['YEAR'].iloc[0], str(dataframe['DOY'].iloc[0]).zfill(3))
            plt.title(title)
            plt.xlabel(xlabel = x_label_name)
            plt.ylabel(ylabel = y_label_name)

            plt.grid(visible = True, axis = 'both', linestyle = '--', linewidth = 1, alpha = 0.4)
            plot = plt.scatter(x = df_aux[x_column_name].values, y = df_aux[y_column_name].values, marker = 's', s = 1)
            # plt.show()

            # https://stackoverflow.com/questions/1841565/valueerror-invalid-literal-for-int-with-base-10
            plt.savefig(self.output_path+'/SubPlots/'+output_file_name+filter_by+str(int(float(i)))+'.png')
            plt.close()


if __name__ == "__main__":
    path_name = f"C:/Users/fengc/OneDrive/Documentos/WP0_RCVR_ANALYSIS/SCEN/SCEN_TLSA00615-GPSL1-SPP/OUT/LOS/TLSA00615_LosInfo_5s.dat"
    dict = read_fields_file(path_name)
    LOS_graph = LOS_Charts(fill_data_fields(dict, path_name))

    light_speed = 299792458
    frecuency_L1 = 1575.42
    
    x_pos_receiver = 4637952.29175333
    y_pos_receiver = 121207.93198126
    z_pos_receiver = 4362375.76379941

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
    dataframe['Tau[ms]'] = dataframe['TROPO[m]']/light_speed

    # T5.4
    dataframe['R_LOS[m]'] = (dataframe['SAT-X[m]']**2 + dataframe['SAT-Y[m]']**2 + dataframe['SAT-Z[m]']**2)**0.5 - (x_pos_receiver**2 + y_pos_receiver**2 + z_pos_receiver**2)**0.5
    dataframe['V_LOS[m]'] = dataframe['ABS_VEL[m]'] * ( dataframe['R_LOS[m]'] / abs(dataframe['R_LOS[m]']) )
    dataframe['F_Doppler'] = - ( dataframe['V_LOS[m]']/light_speed ) * frecuency_L1

    # T5.5
    dataframe['RES[km]'] = dataframe['MEAS[m]']/1000 - (dataframe['RANGE[m]']/1000 - dataframe['CLK_P1[km]'] + dataframe['STEC[m]']/1000 + dataframe['TROPO[m]']/1000)

    LOS_graph.set_dataframe(df = dataframe)

    # ------------------------------------------------- T2 ----------------------------------------------------------------------------
    # """
    # T2.1. Satellite Visibility Periods
    # """
    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'PRN', color_bar_column_name = 'ELEV', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = False, title_plot = "Satellite Visibility", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'GPS-PRN', color_bar_label_name = 'Elevation [deg]'
    #                        )
    
    # """
    # T2.2. Satellite Geometrical Range
    # """
    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'RANGE[m]', color_bar_column_name = 'ELEV', y_div = 1000, \
    #                        default_x_ticks = True, default_y_ticks = True, title_plot = "Satellite Geometical Range", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'RANGE[km]', color_bar_label_name = 'Elevation [deg]'
    #                        )

    # """
    # T2.3. Satellite Tracks
    # """
    # LOS_graph.plot_scatterplot_in_map(x_pos_column = 'SAT-X[m]', y_pos_column = 'SAT-Y[m]', z_pos_column = 'SAT-Z[m]', color_bar_column_name = 'ELEV', \
    #                               title_plot = 'Satellite Tracks during visibility periods', color_bar_label_name ='Elevation [deg]')
    
    # """
    # T2.4. Satellite Velocity
    # """ 
    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'ABS_VEL[m]', color_bar_column_name = 'ELEV', y_div = 1000, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Satellite Range Velocity", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'Absolute Velocity [km/s]', color_bar_label_name = 'Elevation [deg]'
    #                        )
    
    """
    T2.5 NAV Satellite Clock
    """
    LOS_graph.plot_multiple_sub_scatterplot(x_column_name = 'Hour', y_column_name = 'SV-CLK[m]', y_div = 1, filter_by = 'PRN', default_x_ticks = True, default_y_ticks = True, title_plot = "NAV CLK", x_label_name = None, y_label_name = None)


    # """
    # T2.6 Satellite Clock
    # """
    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'SV-CLK[m]', color_bar_column_name = 'PRN', y_div = 1000, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Satellite CLK", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'CLK[km]', color_bar_label_name = 'GPS-PRN'
    #                        )

    # """
    # T2.7 Satellite TGD
    # """
    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'CLK_P1[km]', color_bar_column_name = 'PRN', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Satellite CLK + DTR - TGD", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'CLK[km]', color_bar_label_name = 'GPS-PRN'
    #                        )

    # """
    # T2.8 Satellite DTR
    # """
    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'TGD[m]', color_bar_column_name = 'PRN', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Satellite TGD (Total Group Delay)", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'TGD[m]', color_bar_label_name = 'GPS-PRN'
    #                        )
    # """
    # T3.1 STEC vs TIME (ELEV)
    # """
    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'DTR[m]', color_bar_column_name = 'ELEV', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Satellite DTR (Clock Relativistic Effect)", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'DTR[m]', color_bar_label_name = 'Elevation [deg]'
    #                        )
    # """
    # T3.2 PRN vs TIME (STEC)
    # """
    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'STEC[m]', color_bar_column_name = 'ELEV', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Ionispheric Klobuchar Delay (STEC)", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'STEC[m]', color_bar_label_name = 'Elevation [deg]'
    #                        )
    # """
    # T3.3 VTEC vs. Time
    # """
    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'PRN', color_bar_column_name = 'STEC[m]', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Satellite Visibility vs STEC", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'GPS-PRN', color_bar_label_name = 'STEC[m]'
    #                        )
    # """
    # T3.4 PRN vs. TIME
    # (VTEC)
    # """
    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'VTEC[m]', color_bar_column_name = 'ELEV', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Ionosppheric Klobuchar Delays (VTEC)", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'VTEC[m]', color_bar_label_name = 'ELEV'
    #                        )
    # """
    # T4.1 STD vs. Time
    # (Elevation)
    # """
    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'PRN', color_bar_column_name = 'VTEC[m]', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Satellite Visibility vs VTEC", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'GPS-PRN', color_bar_label_name = 'VTEC[m]'
    #                        )

    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'TROPO[m]', color_bar_column_name = 'ELEV', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Slant Tropospheric Delay (STD)", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'TROPO[m]', color_bar_label_name = 'Elevation [deg]'
    #                        )
    
    # """
    # T4.2 ZTD vs. Time
    # (Elevation)
    # """
    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'ZTD', color_bar_column_name = 'ELEV', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Zenith Tropospheric Delays (ZTD)", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'ZTD', color_bar_label_name = 'Elevation [deg]'
    #                        )
    
    # """
    # T5.1 PSR vs Time
    # """
    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'MEAS[m]', color_bar_column_name = 'ELEV', y_div = 1000, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Pseudo-range C1C vs Time", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'MEAS[Km]', color_bar_label_name = 'Elevation [deg]'
    #                        )

    # """
    # T5.2 TAU vs Time
    # """
    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'Tau[ms]', color_bar_column_name = 'ELEV', y_div = 1000, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "TAU=Rho/c", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'Tau[ms]', color_bar_label_name = 'Elevation [deg]'
    #                        )


    # """
    # T5.3 ToF vs Time
    # """
    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'TOF[ms]', color_bar_column_name = 'ELEV', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Time of Flight (ToF)", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'TOF[ms]', color_bar_label_name = 'Elevation [deg]'
    #                        )
    
    # """
    # T5.4 Doppler
    # Frequency
    # """
    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'F_Doppler', color_bar_column_name = 'ELEV', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Doppler Frequency", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'Doppler Frequency [kHz]', color_bar_label_name = 'Elevation [deg]'
    #                        )


    # """
    # T5.5 Residuals C1
    # """
    # LOS_graph.plot_scatterplot(x_column_name = 'Hour', y_column_name = 'RES[km]', color_bar_column_name = 'PRN', y_div = 1, \
    #                        default_x_ticks = False, default_y_ticks = True, title_plot = "Residuals C1C vs Time", \
    #                        x_label_name = 'Hour of DoY', y_label_name = 'Residuals [km]', color_bar_label_name = 'GPS-PRN'
    #                        )


