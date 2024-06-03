#!/usr/bin/env python39

# Author: Hao Feng Chen Fu

import sys, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import math

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
    
 
"""
T2.1. Satellite Visibility Periods
"""
def plot_satellite_visibility(df):
    dataframe = df[['SOD', 'PRN', 'ELEV']]
    dataframe['SOD'] = dataframe['SOD']/(3600)

    plt.figure()

    plt.xlim(left = 0, right =  24)
    plt.xticks(ticks = range(1, 24))

    plt.ylim(bottom = 0, top = (int(max(dataframe['PRN'].values))+1) )
    plt.yticks(ticks = sorted(dataframe['PRN'].unique()))

    title = 'Satellite Visibility from TLSA on Year 2015 and DoY 006'
    plt.title(title)
    plt.xlabel(xlabel = 'Hour of DoY 006')
    plt.ylabel(ylabel = 'GPS-PRN')

    plt.grid(visible = True, axis = 'both', linestyle = '--', linewidth = 1, alpha = 0.4)

    # Markers: https://matplotlib.org/stable/api/markers_api.html
    plot = plt.scatter(x = dataframe['SOD'].values, y = dataframe['PRN'].values, c = dataframe['ELEV'].values, cmap='gnuplot', marker = 's', s = 1,
                )
    cbar = plt.colorbar(plot)
    cbar.set_label('Elevation [deg]')

    # plt.show()
    plt.savefig(title+'.png')


"""
T2.2. Satellite Geometrical Range
"""
def plot_geometrical_range(df):
    dataframe = df[['SOD', 'RANGE[m]', 'ELEV']]
    dataframe['SOD'] = dataframe['SOD']/(3600)
    dataframe['RANGE[m]'] = dataframe['RANGE[m]']/1000

    plt.figure()

    plt.xlim(left = 0, right =  24)
    plt.xticks(ticks = range(1, 24))

    title = 'Satellite Geometical Range from TLSA on Year 2015 and DoY 006'
    plt.title(title)
    plt.xlabel(xlabel = 'Hour of DoY 006')
    plt.ylabel(ylabel = 'Range[km]')

    plt.grid(visible = True, axis = 'both', linestyle = '--', linewidth = 1, alpha = 0.4)

    # Markers: https://matplotlib.org/stable/api/markers_api.html
    plot = plt.scatter(x = dataframe['SOD'].values, y = dataframe['RANGE[m]'].values, c = dataframe['ELEV'].values, cmap='gnuplot', s = 1)
    cbar = plt.colorbar(plot)
    cbar.set_label('Elevation [deg]')

    # plt.show()
    plt.savefig(title+'.png')


"""
T2.3. Satellite Tracks
"""
def plot_satellite_longitud_altitude(df):
    dataframe = df[['SOD', 'SAT-X[m]', 'SAT-Y[m]', 'SAT-Z[m]', 'ELEV']]

    dataframe['LON'] = np.degrees(np.arctan2(dataframe['SAT-Y[m]'], dataframe['SAT-X[m]']))
    dataframe['LAT'] = np.degrees(np.arcsin(df['SAT-Z[m]'] / np.sqrt(df['SAT-X[m]']**2 + df['SAT-Y[m]']**2 + df['SAT-Z[m]']**2)))
    
    fig = plt.figure(figsize=(18, 10))
    ax = fig.add_subplot()
    # https://naturaldisasters.ai/posts/python-geopandas-world-map-tutorial/
    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

    drop_idxs = world["continent"].isin([
        "Antarctica",
        "Seven seas (open ocean)"
    ])

    world = world.drop(world[drop_idxs].index)
    
    world.plot(
        ax=ax,
        color="lightgray",
        edgecolor="black",
        alpha=0.25,
        # figsize=(15, 10)
    )

    plot = plt.scatter(x = dataframe['LON'].values, y = dataframe['LAT'], c = dataframe['ELEV'].values, cmap='gnuplot', s = 1)
    cbar = plt.colorbar(plot, shrink = 0.5)
    cbar.set_label('Elevation [deg]')
    title = 'Satellite Track during visibility periods from TLSA on Year 2015 DoY 006'
    plt.title(title)
    # plt.show()
    plt.savefig(title+'.png')


"""
T2.4. Satellite Velocity
"""
def plot_satellite_speed(df):
    dataframe = df[['SOD', 'VEL-X[m/s]', 'VEL-Y[m/s]', 'VEL-Z[m/s]', 'ELEV']]
    dataframe['SOD'] = dataframe['SOD']/(3600)
    dataframe['ABS_VEL'] = ((dataframe['VEL-X[m/s]']/1000)**2 + (dataframe['VEL-Y[m/s]']/1000)**2 + (dataframe['VEL-Z[m/s]']/1000)**2)**0.5

    plt.figure()

    plt.xlim(left = 0, right =  24)
    plt.xticks(ticks = range(1, 24))

    title = 'Satellite Range Velocity from TLSA on Year 2015 and DoY 006'
    plt.title(title)
    plt.xlabel(xlabel = 'Hour of DoY 006')
    plt.ylabel(ylabel = 'Absolute Velocity [km/s]')

    plt.grid(visible = True, axis = 'both', linestyle = '--', linewidth = 1, alpha = 0.4)

    # Markers: https://matplotlib.org/stable/api/markers_api.html
    plot = plt.scatter(x = dataframe['SOD'].values, y = dataframe['ABS_VEL'].values, c = dataframe['ELEV'].values, cmap='gnuplot', s = 1)
    cbar = plt.colorbar(plot)
    cbar.set_label('Elevation [deg]')

    plt.show()
    plt.savefig(title+'.png')

# -----------------------------------------------------------------------------------------------------------------------------------------------------------
"""

T2.5 NAV Satellite Clock
In process

Each PRN has its own CLK, filter the clock per PRN,
like PRN19


"""
def plot_satellite_clock(df):
    dataframe = df[['SOD', 'SV-CLK[m]', 'PRN']]
    dataframe['SOD'] = dataframe['SOD']/(3600)
    dataframe['SV-CLK[km]'] = dataframe['SV-CLK[m]']/(1000)

    dataframe[['PRN']] = dataframe[['PRN']].astype(str)

    list_PRN = list(dataframe['PRN'].unique())

    for i in list_PRN:
        df_aux = dataframe[dataframe['PRN'].str.contains(i)]

        df_aux[['PRN']] = df_aux[['PRN']].astype(int)
        
        title = 'PRN {} NAV CLK from TLSA on Year 2015 DoY 006'.format(i)
        plt.figure()

        plt.xlim(left = 0, right =  24)
        plt.xticks(ticks = range(1, 24))

        plt.title(title)
        plt.xlabel(xlabel = 'Hour of DoY 006')
        plt.ylabel(ylabel = 'CLK [km]')

        plt.grid(visible = True, axis = 'both', linestyle = '--', linewidth = 1, alpha = 0.4)
        plt.plot(dataframe['SV-CLK[km]'])
        plt.show()
        
        # plt.savefig('')


# -----------------------------------------------------------------------------------------------------------------------------------------------------------

"""
T2.6 Satellite Clock
"""


"""
T2.7 Satellite TGD
"""
def plot_satellite_TGD(df):
    dataframe = df[['SOD', 'PRN', 'TGD[m]']]
    dataframe['SOD'] = dataframe['SOD']/(3600)

    plt.figure()

    plt.xlim(left = 0, right =  24)
    plt.xticks(ticks = range(1, 24))

    title = 'Satellite TGD (Total Group Delay) from TLSA on Year 2015 and DoY 006'
    plt.title(title)
    plt.xlabel(xlabel = 'Hour of DoY 006')
    plt.ylabel(ylabel = 'TGD[m]')

    plt.grid(visible = True, axis = 'both', linestyle = '--', linewidth = 1, alpha = 0.4)

    # Markers: https://matplotlib.org/stable/api/markers_api.html
    plot = plt.scatter(x = dataframe['SOD'].values, y = dataframe['TGD[m]'].values, c = dataframe['PRN'].values, cmap='gnuplot', marker = 's', s = 0.5,
                )
    cbar = plt.colorbar(plot)
    cbar.set_label('GPS-PRN')

    # plt.show()
    plt.savefig(title+'.png')



"""
T2.8 Satellite DTR
"""
def plot_satellite_DTR(df):
    dataframe = df[['SOD', 'DTR[m]', 'ELEV']]
    dataframe['SOD'] = dataframe['SOD']/(3600)

    plt.figure()

    plt.xlim(left = 0, right =  24)
    plt.xticks(ticks = range(1, 24))

    title = 'Satellite DTR (Clock Relativistic Effect) from TLSA on Year 2015 and DoY 006'
    plt.title(title)
    plt.xlabel(xlabel = 'Hour of DoY 006')
    plt.ylabel(ylabel = 'DTR[m]')

    plt.grid(visible = True, axis = 'both', linestyle = '--', linewidth = 1, alpha = 0.4)

    plot = plt.scatter(x = dataframe['SOD'].values, y = dataframe['DTR[m]'].values, c = dataframe['ELEV'].values, cmap='gnuplot', marker = 's', s = 0.5,
                )
    cbar = plt.colorbar(plot)
    cbar.set_label('Elevation [deg]')

    # plt.show()
    plt.savefig(title+'.png')




"""
T3.1 STEC vs TIME (ELEV)
"""
def plot_satellite_STEC(df):
    dataframe = df[['SOD', 'STEC[m]', 'ELEV']]
    dataframe['SOD'] = dataframe['SOD']/(3600)

    plt.figure()

    plt.xlim(left = 0, right =  24)
    plt.xticks(ticks = range(1, 24))

    title = 'Ionispheric Klobuchar Delay (STEC) from TLSA on Year 2015 and DoY 006'
    plt.title(title)
    plt.xlabel(xlabel = 'Hour of DoY 006')
    plt.ylabel(ylabel = 'STEC[m]')

    plt.grid(visible = True, axis = 'both', linestyle = '--', linewidth = 1, alpha = 0.4)

    plot = plt.scatter(x = dataframe['SOD'].values, y = dataframe['STEC[m]'].values, c = dataframe['ELEV'].values, cmap='gnuplot', marker = 's', s = 0.5,
                )
    cbar = plt.colorbar(plot)
    cbar.set_label('Elevation [deg]')

    plt.show()
    plt.savefig(title+'.png')



"""
T3.2 PRN vs TIME (STEC)
"""
def plot_satellite_visibility_STEC(df):
    dataframe = df[['SOD', 'PRN', 'STEC[m]']]
    dataframe['SOD'] = dataframe['SOD']/(3600)

    plt.figure()

    plt.xlim(left = 0, right =  24)
    plt.xticks(ticks = range(1, 24))

    plt.ylim(bottom = 0, top = (int(max(dataframe['PRN'].values))+1) )
    plt.yticks(ticks = sorted(dataframe['PRN'].unique()))

    title = 'Satellite Visibility vs STEC from TLSA on Year 2015 and DoY 006'
    plt.title(title)
    plt.xlabel(xlabel = 'Hour of DoY 006')
    plt.ylabel(ylabel = 'GPS-PRN')

    plt.grid(visible = True, axis = 'both', linestyle = '--', linewidth = 1, alpha = 0.4)

    # Markers: https://matplotlib.org/stable/api/markers_api.html
    plot = plt.scatter(x = dataframe['SOD'].values, y = dataframe['PRN'].values, c = dataframe['STEC[m]'].values, cmap='gnuplot', marker = 's', s = 1,
                )
    cbar = plt.colorbar(plot)
    cbar.set_label('STEC[m]')

    # plt.show()
    plt.savefig(title+'.png')


"""
T3.3 VTEC vs. Time
"""



"""
T3.4 PRN vs. TIME
(VTEC)
"""
def plot_satellite_visibility_VTEC(df):
    dataframe = df[['SOD', 'ELEV', 'VTEC[m]']]
    dataframe['SOD'] = dataframe['SOD']/(3600)

    plt.figure()

    plt.xlim(left = 0, right =  24)
    plt.xticks(ticks = range(1, 24))

    title = 'Satellite Visibility vs VTEC from TLSA on Year 2015 and DoY 006'
    plt.title(title)
    plt.xlabel(xlabel = 'Hour of DoY 006')
    plt.ylabel(ylabel = 'GPS-PRN')

    plt.grid(visible = True, axis = 'both', linestyle = '--', linewidth = 1, alpha = 0.4)

    # Markers: https://matplotlib.org/stable/api/markers_api.html
    plot = plt.scatter(x = dataframe['SOD'].values, y = dataframe['VTEC[m]'].values, c = dataframe['ELEV'].values, cmap='gnuplot', marker = 's', s = 1,
                )
    cbar = plt.colorbar(plot)
    cbar.set_label('ELEV')

    plt.show()
    plt.savefig(title+'.png')




"""

"""
def plot_satellite_STD(df):
    dataframe = df[['SOD', 'ELEV', 'TROPO[m]']]
    dataframe['SOD'] = dataframe['SOD']/(3600)

    plt.figure()

    plt.xlim(left = 0, right =  24)
    plt.xticks(ticks = range(1, 24))

    title = 'Satellite Visibility vs VTEC from TLSA on Year 2015 and DoY 006'
    plt.title(title)
    plt.xlabel(xlabel = 'Hour of DoY 006')
    plt.ylabel(ylabel = 'GPS-PRN')

    plt.grid(visible = True, axis = 'both', linestyle = '--', linewidth = 1, alpha = 0.4)

    # Markers: https://matplotlib.org/stable/api/markers_api.html
    plot = plt.scatter(x = dataframe['SOD'].values, y = dataframe['TROPO[m]'].values, c = dataframe['ELEV'].values, cmap='gnuplot', marker = 's', s = 1,
                )
    cbar = plt.colorbar(plot)
    cbar.set_label('ELEV')
    plt.savefig('TROPO_STD_vs_TIME_TLSA_D006Y15.png')


if __name__ == "__main__":
    path_name = f"C:/Users/fengc/OneDrive/Documentos/WP0_RCVR_ANALYSIS/SCEN/SCEN_TLSA00615-GPSL1-SPP/OUT/LOS/TLSA00615_LosInfo_5s.dat"
    dict = read_fields_file(path_name)
    dataframe = fulfill_dict_fields(dict, path_name)

    ## ------- T2 ----------
    # plot_satellite_visibility(dataframe)
    # plot_geometrical_range(dataframe)
    # plot_satellite_longitud_altitude(dataframe)
    # plot_satellite_speed(dataframe)


    # plot_satellite_clock(dataframe)     # IN PROCESS
    # plot_satellite_TGD(dataframe)
    # plot_satellite_DTR(dataframe)
    # plot_satellite_STEC(dataframe)

    ## ------- T3 ----------
    # plot_satellite_visibility_STEC(dataframe)
    plot_satellite_visibility_VTEC(dataframe)           # NOT CORRECT

    ## ------- T4 ----------
    plot_satellite_STD(dataframe)