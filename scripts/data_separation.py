from imported_func import *
###### Separate reanalyses and form lists accordingly ######
def reanalyses_separation(inp, i):
    # doc-string
    inp_temp = copy.deepcopy(inp.get(i))
    inp_temp_era5 = inp_temp[:6120]  # full length (all 40 years) 6120
    inp_temp_erai = inp_temp[6120:11475]  # full length (all 40 years) 11475
    inp_temp_jra55 = inp_temp[11475:16830]  # full length (all 40 years) 16830
    inp_temp_merra = inp_temp[16830:]
    return inp_temp_era5, inp_temp_erai, inp_temp_jra55, inp_temp_merra

def reanalyses_separation_extr(inp, i):
    inp_temp = copy.deepcopy(inp.get(i))
    inp_temp_era5 = inp_temp[:213]
    inp_temp_erai = inp_temp[213:213+110]
    inp_temp_jra55 = inp_temp[213+110:213+110+110]
    inp_temp_merra = inp_temp[213+110+110:]
    return inp_temp_era5, inp_temp_erai, inp_temp_jra55, inp_temp_merra

def get_lists_reanalysis(dic, dic_extr):
    # doc-string
    inp_era5 = []; inp_erai = []; inp_jra55 = []; inp_merra = []
    inp_extr_era5 = []; inp_extr_erai = []; inp_extr_jra55 = []; inp_extr_merra = []
    for i in range(4):
        inp_era5_temp, inp_erai_temp, inp_jra55_temp, inp_merra_temp = reanalyses_separation(dic, i)
        inp_extr_era5_temp, inp_extr_erai_temp, inp_extr_jra55_temp, inp_extr_merra_temp = reanalyses_separation_extr(dic_extr, i)

        inp_era5.append(inp_era5_temp); inp_extr_era5.append(inp_extr_era5_temp)
        inp_erai.append(inp_erai_temp); inp_extr_erai.append(inp_extr_erai_temp)
        inp_jra55.append(inp_jra55_temp); inp_extr_jra55.append(inp_extr_jra55_temp)
        inp_merra.append(inp_merra_temp); inp_extr_merra.append(inp_extr_merra_temp)


    return inp_era5, inp_erai, inp_jra55, inp_merra, inp_extr_era5, inp_extr_erai, inp_extr_jra55, inp_extr_merra

###### Separate reanalyses and form lists accordingly ######

def models_separation_cmip5(inp, i, sep):
    inp_temp = copy.deepcopy(inp.get(i))
    inp_temp_cnrm = inp_temp[:sep]
    inp_temp_gfdl = inp_temp[sep:sep*2]
    inp_temp_miroc = inp_temp[sep*2:]
    return inp_temp_cnrm, inp_temp_gfdl, inp_temp_miroc

def models_separation_extr_cmip5(inp, i):
    inp_temp = copy.deepcopy(inp.get(i))
    inp_temp_cnrm = inp_temp[:132]
    inp_temp_gfdl = inp_temp[132: 132 + 111]
    inp_temp_miroc = inp_temp[132 + 111:]
    return inp_temp_cnrm, inp_temp_gfdl, inp_temp_miroc

def get_lists_cmip5(dic_cmip5, dic_extr_cmip5):
    inp_cnrm = []; inp_gfdl = []; inp_miroc = []
    inp_extr_cnrm = []; inp_extr_gfdl = []; inp_extr_miroc = []

    # RCP
    # inp_cnrm_rcp = []; inp_gfdl_rcp = []; inp_miroc_rcp = []
    # inp_extr_cnrm_rcp = []; inp_extr_gfdl_rcp = []; inp_extr_miroc_rcp = []

    for i in range(4):
        inp_cnrm_temp, inp_gfdl_temp, inp_miroc_temp = models_separation_cmip5(dic_cmip5, i, 4131)
        inp_extr_cnrm_temp, inp_extr_gfdl_temp, inp_extr_miroc_temp = models_separation_extr_cmip5(dic_extr_cmip5, i)

        # inp_cnrm_temp_rcp, inp_gfdl_temp_rcp, inp_miroc_temp_rcp = models_separation_cmip5(dic_cmip5, i, 4131)
        # inp_extr_cnrm_temp_rcp, inp_extr_gfdl_temp_rcp, inp_extr_miroc_temp_rcp = models_separation_extr_cmip5(dic_extr_cmip5, i)

        inp_cnrm.append(inp_cnrm_temp); inp_extr_cnrm.append(inp_extr_cnrm_temp)
        inp_gfdl.append(inp_gfdl_temp); inp_extr_gfdl.append(inp_extr_gfdl_temp)
        inp_miroc.append(inp_miroc_temp); inp_extr_miroc.append(inp_extr_miroc_temp)

    return inp_cnrm, inp_gfdl, inp_miroc, inp_extr_cnrm, inp_extr_gfdl, inp_extr_miroc

# the same with amip simulations
def models_separation_amip(inp, i, sep):
    inp_temp = copy.deepcopy(inp.get(i))
    inp_temp_cnrm = inp_temp[:sep]
    inp_temp_gfdl = inp_temp[sep:sep * 2]
    inp_temp_miroc = inp_temp[sep*2:sep*3]
    inp_temp_mpi = inp_temp[sep*3:sep*4]
    #inp_temp_earth = inp_temp[sep * 4:]
    return inp_temp_cnrm, inp_temp_gfdl, inp_temp_miroc, inp_temp_mpi#, inp_temp_earth

def models_separation_extr_amip(inp, i):
    inp_temp = copy.deepcopy(inp.get(i))
    inp_temp_cnrm = inp_temp[:102]
    inp_temp_gfdl = inp_temp[102:102+109]
    inp_temp_miroc = inp_temp[102+109:102+109+135]
    inp_temp_mpi = inp_temp[102+109+135:102+109+135+138]
    #inp_temp_earth = inp_temp[102+109+135+138:]
    return inp_temp_cnrm, inp_temp_gfdl, inp_temp_miroc, inp_temp_mpi#, inp_temp_earth


def get_lists_amip(dic_amip, dic_extr_amip):
    inp_amip_cnrm = []; inp_amip_gfdl = []; inp_amip_miroc = []; inp_amip_mpi = []; inp_amip_earth = []
    inp_amip_extr_cnrm = []; inp_amip_extr_gfdl = []; inp_amip_extr_miroc = []
    inp_amip_extr_mpi = []#; inp_amip_extr_earth = []
    for i in range(4):
        # inp_amip_cnrm_temp, inp_amip_gfdl_temp, inp_amip_miroc_temp, inp_amip_mpi_temp, inp_amip_earth_temp = models_separation_amip(dic_amip, i, 4131)
        # inp_amip_extr_cnrm_temp, inp_amip_extr_gfdl_temp, inp_amip_extr_miroc_temp, \
        # inp_amip_extr_mpi_temp, inp_amip_extr_earth_temp = models_separation_extr_amip(dic_extr_amip, i)

        inp_amip_cnrm_temp, inp_amip_gfdl_temp, inp_amip_miroc_temp, inp_amip_mpi_temp = models_separation_amip(dic_amip, i, 4131)
        inp_amip_extr_cnrm_temp, inp_amip_extr_gfdl_temp, inp_amip_extr_miroc_temp, \
        inp_amip_extr_mpi_temp = models_separation_extr_amip(dic_extr_amip, i)

        inp_amip_cnrm.append(inp_amip_cnrm_temp); inp_amip_extr_cnrm.append(inp_amip_extr_cnrm_temp)
        inp_amip_gfdl.append(inp_amip_gfdl_temp); inp_amip_extr_gfdl.append(inp_amip_extr_gfdl_temp)
        inp_amip_miroc.append(inp_amip_miroc_temp); inp_amip_extr_miroc.append(inp_amip_extr_miroc_temp)
        inp_amip_mpi.append(inp_amip_mpi_temp); inp_amip_extr_mpi.append(inp_amip_extr_mpi_temp)
        #inp_amip_earth.append(inp_amip_earth_temp); inp_amip_extr_earth.append(inp_amip_extr_earth_temp)

    return inp_amip_cnrm, inp_amip_gfdl, inp_amip_miroc, inp_amip_mpi, \
           inp_amip_extr_cnrm, inp_amip_extr_gfdl, inp_amip_extr_miroc, inp_amip_extr_mpi#, inp_amip_extr_earth

# the same with rcp4.5 simulations
def models_separation_extr_cmip5_rcp45(inp, i):
    inp_temp = copy.deepcopy(inp.get(i))
    # inp_temp_cnrm = inp_temp[:3756]
    # inp_temp_gfdl = inp_temp[3756: 3756 + 4524]
    # inp_temp_miroc = inp_temp[3756 + 4524:]
    inp_temp_cnrm = inp_temp[:124]
    inp_temp_gfdl = inp_temp[124: 124 + 117]
    inp_temp_miroc = inp_temp[124 + 117:]
    return inp_temp_cnrm, inp_temp_gfdl, inp_temp_miroc

def get_lists_cmip5_rcp45(dic_cmip5, dic_extr_cmip5):
    inp_cnrm = []; inp_gfdl = []; inp_miroc = []
    inp_extr_cnrm = []; inp_extr_gfdl = []; inp_extr_miroc = []

    for i in range(4):
        inp_cnrm_temp, inp_gfdl_temp, inp_miroc_temp = models_separation_cmip5(dic_cmip5, i, 4743)
        inp_extr_cnrm_temp, inp_extr_gfdl_temp, inp_extr_miroc_temp = models_separation_extr_cmip5_rcp45(dic_extr_cmip5, i)

        inp_cnrm.append(inp_cnrm_temp); inp_extr_cnrm.append(inp_extr_cnrm_temp)
        inp_gfdl.append(inp_gfdl_temp); inp_extr_gfdl.append(inp_extr_gfdl_temp)
        inp_miroc.append(inp_miroc_temp); inp_extr_miroc.append(inp_extr_miroc_temp)

    return inp_cnrm, inp_gfdl, inp_miroc, inp_extr_cnrm, inp_extr_gfdl, inp_extr_miroc
