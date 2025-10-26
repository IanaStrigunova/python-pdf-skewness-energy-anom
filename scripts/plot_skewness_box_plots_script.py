#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plotting PDFs (Probability Density FUnctions)
for ERA5 and CMIP5 datasets (climatology and during EHWs)

@author: Iana Strigunova
"""
import importlib
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import plot_skewness_box_plots_src
from plot_skewness_box_plots_src import *
importlib.reload(plot_skewness_box_plots_src)
#sns.set_style("white")
sns.set_style("ticks")
sns.set_context("paper")
plt.rcParams['axes.grid'] = False

## adjust path according to where files are stored
path_to_files = "data\\"
# list of atmospheric flows analysed here with specified order
labels_flows = ['total', 'zonal flow', 'planetary', 'synoptic']

###########################Reading files of normaised energy anomalies###################################################################
print('Reading files of normaised energy anomalies')
filename_clim = "norm_energy_anomalies_allrean_allflows.txt"
filename_extr = "norm_energy_anomalies_allrean_allflows_extremes.txt"
dic_allflows, dic_allflows_extr = dict_norm_anomalies(path_to_files, filename_clim, filename_extr)

filename_clim_cmip5 = "norm_energy_anomalies_cmip5_allflows_trop_barotrop.txt"
filename_extr_cmip5 = "norm_energy_anomalies_cmip5_allflows_extremes_trop_barotrop.txt"
dic_allflows_cmip5, dic_allflows_extr_cmip5 = dict_norm_anomalies(path_to_files, filename_clim_cmip5, filename_extr_cmip5)

filename_clim_cmip5_rcp = "norm_energy_anomalies_cmip5_allflows_trop_barotrop_rcp45.txt"
filename_extr_cmip5_rcp = "norm_energy_anomalies_cmip5_allflows_extremes_trop_barotrop_rcp45.txt"
dic_allflows_cmip5_rcp, dic_allflows_extr_cmip5_rcp = dict_norm_anomalies(path_to_files, filename_clim_cmip5_rcp, filename_extr_cmip5_rcp)

filename_clim_amip = "norm_energy_anomalies_cmip5_amip_allflows_trop_barotrop.txt"
filename_extr_amip = "norm_energy_anomalies_cmip5_amip_allflows_extremes_trop_barotrop.txt"
dic_allflows_amip, dic_allflows_extr_amip = dict_norm_anomalies(path_to_files, filename_clim_amip, filename_extr_amip)
###########################Reading files of normaised energy anomalies###################################################################

# Focus only on planetary scale (0 - total, 1 - the zonal-mean flow, 2 - planetary, 3 - synoptic)
ind_flow = 2
# Form lists of data for easier handling
all_in_one_clim_rcp = [dic_allflows.get(ind_flow), dic_allflows_cmip5.get(ind_flow),
                       dic_allflows_amip.get(ind_flow), dic_allflows_cmip5_rcp.get(ind_flow)]
all_in_one_extr_rcp = [dic_allflows_extr.get(ind_flow), dic_allflows_extr_cmip5.get(ind_flow),
             dic_allflows_extr_amip.get(ind_flow), dic_allflows_extr_cmip5_rcp.get(ind_flow)]
lbls_annot = ['(a) Reanalyses ', '(b) CMIP5 (HIST)', '(c) CMIP5 (AMIP)', '(d) CMIP5 (RCP4.5)']
pdfs_comparison(all_in_one_clim_rcp, all_in_one_extr_rcp, lbls_annot, "test_pdfs", True)

###########################Recovering fata for each model separately####################################################
## Note that the most of function uses the manual way of reconstrcution.
## It means that one has to know how data were created and make changes in the functions manually.
print('Recovering data for each model separately')
# labels = ['ERA5', 'CNRM', 'GFDL', 'MIROC']
# set color cycler to plot all models and ERA5
# colormap = plt.cm.nipy_spectral  # nipy_spectral_r, gist_ncar, Set1,Paired
# colors = [colormap(i) for i in np.linspace(0.05, 0.95, len(labels))]
# plt.rcParams['axes.prop_cycle'] = cycler.cycler('color', colors)

list_era5, list_erai, list_jra55, list_merra, list_extr_era5, list_extr_erai, list_extr_jra55, list_extr_merra = \
    get_lists_reanalysis(dic_allflows, dic_allflows_extr)  # separation depends on the length of data!

list_cnrm, list_gfdl, list_miroc, list_extr_cnrm, list_extr_gfdl, list_extr_miroc = \
    get_lists_cmip5(dic_allflows_cmip5, dic_allflows_extr_cmip5)

list_cnrm_rcp, list_gfdl_rcp, list_miroc_rcp, list_extr_cnrm_rcp, list_extr_gfdl_rcp, list_extr_miroc_rcp = \
    get_lists_cmip5_rcp45(dic_allflows_cmip5_rcp, dic_allflows_extr_cmip5_rcp)

list_amip_cnrm, list_amip_gfdl, list_amip_miroc, list_amip_mpi,\
list_amip_extr_cnrm, list_amip_extr_gfdl, list_amip_extr_miroc, \
    list_amip_extr_mpi = get_lists_amip(dic_allflows_amip, dic_allflows_extr_amip)
###########################Recovering fata for each model separately###################################################################


###########################Forming lists and dict-like objects to compute boostrapped skewness with further plotting####
print('Forming lists and dict-like objects to compute boostrapped skewness with further plotting')
def bootstrapped_skew_kurt(ref, model):

    sims_sk = np.zeros((1000)); sims_k = np.zeros((1000))
    sims_sk1 = np.zeros((1000)); sims_k1 = np.zeros((1000))

    for k in range(1000):
        # Create a random sample from data
        temp_sample = np.random.choice(ref, replace=True, size=len(ref))
        temp_sample1 = np.random.choice(model, replace=True, size=len(model))
        # Get statistics for random sample
        sample_sk = skew(temp_sample, bias=True)
        sample_k = kurtosis(temp_sample, bias=False)

        sample_sk1 = skew(temp_sample1, bias=True)
        sample_k1 = kurtosis(temp_sample1, bias=False)

        # Add each simulation
        sims_sk[k] += sample_sk
        sims_k[k] += sample_k

        sims_sk1[k] += sample_sk1
        sims_k1[k] += sample_k1

    return sims_sk, sims_k, sims_sk1, sims_k1

## create lists of datasets depending on run
tas_var = [list_era5[ind_flow], list_cnrm[ind_flow], list_amip_cnrm[ind_flow], list_gfdl[ind_flow], list_amip_gfdl[ind_flow],
           list_miroc[ind_flow], list_amip_miroc[ind_flow], list_amip_mpi[ind_flow]]
tas_var_extr = [list_extr_era5[ind_flow], list_extr_cnrm[ind_flow], list_amip_extr_cnrm[ind_flow], list_extr_gfdl[ind_flow], list_amip_extr_gfdl[ind_flow],
           list_extr_miroc[ind_flow], list_amip_extr_miroc[ind_flow], list_amip_extr_mpi[ind_flow]]
tas_var_rcp = [list_era5[ind_flow], list_cnrm[ind_flow], list_cnrm_rcp[ind_flow], list_gfdl[ind_flow], list_gfdl_rcp[ind_flow],
           list_miroc[ind_flow], list_miroc_rcp[ind_flow]]
tas_var_rcp_extr = [list_era5[ind_flow], list_extr_cnrm[ind_flow], list_extr_cnrm_rcp[ind_flow], list_extr_gfdl[ind_flow], list_extr_gfdl_rcp[ind_flow],
           list_extr_miroc[ind_flow], list_extr_miroc_rcp[ind_flow]]

## create empty lists and fill with bootstrapped skewness
sims_sk1 = []; sims_k1 = []; sims_sk1_rcp = []; sims_k1_rcp = []
sims_sk2 = []; sims_k2 = []; sims_sk2_rcp = []; sims_k2_rcp = []

# present
for i in range(len(tas_var)):
    sims_sk, sims_k, sims_sk1_temp, sims_k1_temp = bootstrapped_skew_kurt(dic_allflows.get(ind_flow), tas_var[i])
    sims_sk_extr, sims_k_extr, sims_sk2_temp, sims_k2_temp = bootstrapped_skew_kurt(dic_allflows_extr.get(ind_flow), tas_var_extr[i])

    sims_sk1.append(sims_sk1_temp); sims_k1.append(sims_k1_temp)
    sims_sk2.append(sims_sk2_temp); sims_k2.append(sims_k2_temp)
# future
for i in range(len(tas_var_rcp)):
    sims_sk, sims_k, sims_sk1_temp_rcp, sims_k1_temp_rcp = bootstrapped_skew_kurt(dic_allflows.get(ind_flow),
                                                                                  tas_var_rcp[i])
    sims_sk_extr_rcp, sims_k_extr_rcp, sims_sk2_temp_rcp, sims_k2_temp_rcp = bootstrapped_skew_kurt(
        dic_allflows_extr.get(ind_flow), tas_var_rcp_extr[i])

    sims_sk1_rcp.append(sims_sk1_temp_rcp); sims_k1_rcp.append(sims_k1_temp_rcp)
    sims_sk2_rcp.append(sims_sk2_temp_rcp); sims_k2_rcp.append(sims_k2_temp_rcp)

### set labels (should be identical lists with datasets)
name_lst = ["ERA5", "CNRM-CM5", "GFDL-CM3", "MIROC5"]
name_amip_lst = ["CNRM-CM5", "GFDL-CM3", "MIROC5", "MPI-ESM-LR"]

## fill lists of bootstrapped skewnesses
lst_data_check = [sims_sk, sims_sk_extr, sims_sk1[0], sims_sk2[0],
                  sims_sk1[1], sims_sk2[1],
                  sims_sk1[2], sims_sk2[2], sims_sk1_rcp[2], sims_sk2_rcp[2],
                  sims_sk1[3], sims_sk2[3],
                  sims_sk1[4], sims_sk2[4],  sims_sk1_rcp[4], sims_sk2_rcp[4],
                  sims_sk1[5], sims_sk2[5],
                  sims_sk1[6], sims_sk2[6], sims_sk1_rcp[6], sims_sk2_rcp[6]]
# form lists with labels
names_hws = [name_lst[0], name_lst[0] + "HWs", name_lst[1], name_lst[1] + "HWs",
name_amip_lst[0]+" (AMIP)", name_amip_lst[0]+" (AMIP, HWs)", name_lst[1] + "(RCP4.5)", name_lst[1] + " (RCP4.5, HWs)",
    name_lst[2], name_lst[2] + "HWs", name_amip_lst[1]+" (AMIP)", name_amip_lst[1]+" (AMIP, HWs)",
    name_lst[2] + "(RCP4.5)", name_lst[2] + " (RCP4.5, HWs)", name_lst[3], name_lst[3] + "HWs",
name_amip_lst[2]+" (AMIP)", name_amip_lst[2]+" (AMIP, HWs)", name_lst[3] + "(RCP4.5)", name_lst[3] + " (RCP4.5, HWs)",
             name_amip_lst[3]+" (AMIP)", name_amip_lst[3]+" (AMIP, HWs)",]
# mask some labels for clarity
names_hws_mask = [name_lst[0],"", name_lst[1], "", "(AMIP)", "", "(RCP4.5)", "",
    name_lst[2], "", "(AMIP)", "", "(RCP4.5)", "", name_lst[3], "","(AMIP)", "", "(RCP4.5)", "",
             name_amip_lst[3]+" (AMIP)", "",]
# customise colorbar depending on data
my_pal_lst_hws = ["tab:blue" if val % 2 == 0 else "tab:red" for val in range(len(names_hws))]
my_pal_hws = dict(zip(range(len(names_hws)), my_pal_lst_hws))
# call function that plots data and saves in .png and .eps formats (if flag is set True)
box_plots_skew_clim_hws(lst_data_check, names_hws_mask, my_pal_hws, "Skewness", "Climatology", "EHWs", "test_skew", savefig=True)
###########################Forming lists and dict-like objects to compute boostrapped skewness with further plotting####
