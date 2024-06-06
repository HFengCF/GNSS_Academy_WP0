LOS_scatterplot_data = {
    # Format:
    # x_column, y_column, cbar_column, y_div , default_x_ticks, default_y_ticks, title_plot, x_label, y_label, cbar_label, output_file_name 

    # T2.1
    "Sat_Visibility":['Hour', 'PRN', 'ELEV', 1, False, False, 'Satellite Visibility', 'Hour of DoY', 'GPS-PRN', 'Elevation [deg]', 'SAT_VISIBILITY_TLSA_D006Y15' ],
    # T2.2
    "Sat_Geometrical_Range":['Hour', 'RANGE[m]', 'ELEV', 1000, False, True, 'Satellite Geometrical Range', 'Hour of DoY', 'RANGE[km]', 'Elevation [deg]', 'SAT_GEOMETRICAL_RANGE_TLSA_D006Y15' ],
    # T2.4
    "Sat_Range_Velocity":['Hour', 'ABS_VEL[m]', 'ELEV', 1000, False, True, 'Satellite Range Velocity', 'Hour of DoY', 'Velocity [km]', 'Elevation [deg]', 'SAT_VELOCITY_TLSA_D006Y15' ],
    # T2.6
    "Sat_Clock":['Hour', 'SV-CLK[m]', 'PRN', 1000, False, True, 'Satellite CLK', 'Hour of DoY', 'CLK[km]', 'GPS-PRN', 'SAT_CLK_TLSA_D006Y15_1' ],

    "Sat_Clock_DTR_TGD":['Hour', 'CLK_P1[km]', 'PRN', 1, False, True, 'Satellite CLK + DTR - TGD', 'Hour of DoY', 'CLK[km]', 'GPS-PRN', 'SAT_CLK_TLSA_D006Y15_2' ],
    # T2.7
    "Sat_TGD":['Hour', 'TGD[m]', 'PRN', 1, False, True, 'Satellite TGD (Total Group Delay)', 'Hour of DoY', 'TGD[m]', 'GPS-PRN', 'SAT_TGD_TLSA_D006Y15' ],
    # T2.8
    "Sat_DTR":['Hour', 'DTR[m]', 'ELEV', 1, False, True, 'Satellite DTR (Clock Relativistic Effect)', 'Hour of DoY', 'DTR[m]', 'Elevation [deg]', 'SAT_DTR_TLSA_D006Y15' ],

    # T3.1
    "Sat_STEC":['Hour', 'STEC[m]', 'ELEV', 1, False, True, 'Ionispheric Klobuchar Delay (STEC)', 'Hour of DoY', 'STEC[m]', 'Elevation [deg]', 'IONO_STEC_vs_TIME_TLSA_D006Y15' ],
    # T3.2
    "Sat_Visibility_vs_STEC":['Hour', 'PRN', 'STEC[m]', 1, False, True, 'Satellite Visibility vs STEC', 'Hour of DoY', 'GPS-PRN', 'STEC[m]', 'IONO_STEC_vs_PRN_TLSA_D006Y15' ],
    # T3.3
    "Sat_VTEC_vs_Time":['Hour', 'VTEC[m]', 'ELEV', 1, False, True, 'Ionosppheric Klobuchar Delays (VTEC)', 'Hour of DoY', 'VTEC[m]', 'Elevation [deg]', 'IONO_VTEC_vs_TIME_TLSA_D006Y15' ],
    # T3.4
    "Sat_VTEC_vs_PRN":['Hour', 'PRN', 'VTEC[m]', 1, False, True, 'Satellite Visibility vs VTEC', 'Hour of DoY', 'GPS-PRN', 'VTEC[m]', 'IONO_VTEC_vs_PRN_TLSA_D006Y15.png' ],

    # T4.1
    "Sat_STD":['Hour', 'TROPO[m]', 'ELEV', 1, False, True, 'Slant Tropospheric Delay (STD)', 'Hour of DoY', 'STD[m]', 'Elevation [deg]', 'TROPO_STD_vs_TIME_TLSA_D006Y15' ],
    # T4.2
    "Sat_ZTD":['Hour', 'ZTD', 'ELEV', 1, False, True, 'Zenith Tropospheric Delays (ZTD)', 'Hour of DoY', 'ZTD', 'Elevation [deg]', 'TROPO_ZTD_vs_TIME_TLSA_D006Y15' ],

    # T5.1
    "Sat_PSR_vs_Time":['Hour', 'MEAS[m]', 'ELEV', 1000, False, True, 'Pseudo-range C1C vs Time', 'Hour of DoY', 'MEAS[km]', 'Elevation [deg]', 'MEAS_CODES_vs_TIME_TLSA_D006Y15' ],
    # T5.2
    "Sat_TAU_vs_Time":['Hour', 'Tau[ms]', 'ELEV', 1000, False, True, 'TAU=Rho/c', 'Hour of DoY', 'Tau[ms]', 'Elevation [deg]', 'TAU_vs_TIME_TLSA_D006Y15' ],
    # T5.3
    "Sat_ToF_vs_Time":['Hour', 'TOF[ms]', 'ELEV', 1, False, True, 'Time of Flight (ToF)', 'Hour of DoY', 'TOF[ms]', 'Elevation [deg]', 'ToF_vs_TIME_TLSA_D006Y15' ],
    # T5.4
    "Sat_Doppler":['Hour', 'F_Doppler', 'ELEV', 1, False, True, 'Doppler Frequency', 'Hour of DoY', 'Doppler Frequency [kHz]', 'Elevation [deg]', 'DOPPLER_FREQ_vs_TIME_TLSA_D006Y15' ],
    # T5.5
    "Sat_Residuals":['Hour', 'RES[km]', 'PRN', 1, False, True, 'Residuals C1C vs Time', 'Hour of DoY', 'Residuals[km]', 'GPS-PRN', 'MEAS_RESIDUALS_vs_TIME_TLSA_D006Y15' ],

}

LOS_scatterplot_map_data = {
    "Sat_Tracks": ['SAT-X[m]', 'SAT-Y[m]', 'SAT-Z[m]', 'ELEV', 'Satellite Tracks during visibility periods', 'Elevation [deg]']
}

LOS_CLK_scatter_plots = {
    "Sat_Clock": ['Hour', 'SV-CLK[m]', 'PRN', True, True, 'NAV CLK', 'Hour of DoY', 'CLK[km]', 'SAT_CLK_TLSA_D006Y15_']
}

POS_plots = {
    "Sat_number": ['Hour', 'Hour of DoY', 'Number of Satellites', "Number of Satellites in PVT vs Time", 'NSATS'],
    "DOPs": ['Hour', 'Hour of DoY', 'DOP', "Dilution of Precision (DOP)", 'GDOP', 'PDOP', 'TDOP'],
    "H_V DOPs": ['Hour', 'Hour of DoY', 'DOP', "Dilution of Precision (DOP)", 'HDOP', 'VDOP', 'NSATS'],
    "ENU": ['Hour', 'Hour of DoY', 'ENU_PM[m]', "ENU Position Error", 'UPE[m]', 'EPE[m]', 'NPE[m]'],
    "HPE_VPE": ['Hour', 'Hour of DoY', 'H/VPE[m]', "HPE-VPE Position Error", 'VPE', 'HPE']

}
POS_scatterplot = {
    "EPE_NPE": ['EPE[m]', 'NPE[m]', 'HDOP', 1, False, True, "EPE vs NPE", 'EPE[m]', 'NPE[m]', 'HDOP', 'POS_NPE_vs_EPE_TLSA_D006Y15']
    
}

print(LOS_scatterplot_data)