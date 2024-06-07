import sys, os
from POS_chart import POS_Charts
from LOS_chart import LOS_Charts

import features

from search_file import read_fields_file, fill_data_fields

def main():
    
    # Scen_path = sys.argv[1]

    # folder_output = Scen_path + '\OUTPUT_SCEN_TLSA00615-GPSL1-SPP'

    # print('Path: ', folder_output)
    # if not os.path.exists(folder_output):
    #     os.makedirs(folder_output)

    path_name = f"C:/Users/fengc/OneDrive/Documentos/WP0_RCVR_ANALYSIS/SCEN/SCEN_TLSA00615-GPSL1-SPP/OUT/POS/TLSA00615_PosInfo_5s.dat"
    dict = read_fields_file(path_name)
    POS_graph = POS_Charts(fill_data_fields(dict, path_name))

    dataframe = POS_graph.get_dataframe()
    dataframe['HPE'] = (dataframe['EPE[m]']**2 + dataframe['NPE[m]']**2)**0.5
    dataframe['VPE'] = abs(dataframe['UPE[m]'])
    POS_graph.set_dataframe(df = dataframe)

    for key, value in features.POS_plots.items():
        pos_args = value[:5]
        kw_args = {}

        if len(value) > 5:
            extra_args = value[5:]
            for i, extra_arg in enumerate(extra_args):
                kw_args[f'kwarg{i+1}'] = extra_arg

        POS_graph.plot_linearplot(*pos_args, **kw_args)


def generate_POS_figures():
    path_name = f"C:/Users/fengc/OneDrive/Documentos/WP0_RCVR_ANALYSIS/SCEN/SCEN_TLSA00615-GPSL1-SPP/OUT/POS/TLSA00615_PosInfo_5s.dat"
    dict = read_fields_file(path_name)
    POS_graph = POS_Charts(fill_data_fields(dict, path_name))

    dataframe = POS_graph.get_dataframe()
    dataframe['HPE'] = (dataframe['EPE[m]']**2 + dataframe['NPE[m]']**2)**0.5
    dataframe['VPE'] = abs(dataframe['UPE[m]'])
    POS_graph.set_dataframe(df = dataframe)

    # for key, value in features.POS_plots.items():
    #     pos_args = value[:4]
    #     kw_args = {}

    #     if len(value) > 5:
    #         extra_args = value[5:]
    #         for i, extra_arg in enumerate(extra_args):
    #             kw_args[f'kwarg{i+1}'] = extra_arg

    #     POS_graph.plot_linearplot(*pos_args, **kw_args)

    for key, value in features.POS_scatterplot():
        POS_graph.plot_scatterplot_POS(*value)


if __name__ == "__main__":
    main()