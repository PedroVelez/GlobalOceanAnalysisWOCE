import os
import cartopy.feature
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import datetime
from ftplib import FTP
import pandas as pd
from tqdm import tqdm
import gsw
import glob
"""For this code is important to take into account the quality control falgs for the different variables. According to the WOCE web site, the quality control flags are the following:
0 : Not assigned
1 : Not calibrated
2: Acceptable measurementç
3 : Questionable measurement
4 : Bad measurement
5 : Not reported
6 : Interpolated over a pressure interval larger than 2 dbar.
7 : despiked
8 : Not used for ctd data
9 : Not sampled
With these flags on mind and after some inspection of the data, we have concluded that the best way to proceed is only keep the data with qc = 0 , 1 and 2
"""

# Creating a dictionary with the comments for each file
# File : Comment
comments ={
    "64PE20000926_ctd.nc": "Shared with AR07, but section_id = [A1E/AR7E], labeled as A01",
    "5_58GS20150410_ctd.nc": "Unique but section_id was wrong",
    "31RBOACES24N_2_ctd.nc": "Shared with AR01, but section_id = [AR01], labeled as A05",
    "29AH20110128_ctd.nc": "Unique but section_id was wrong",
    "6_74EQ20220209_ctd.nc": "Unique but section_id was wrong",
    "740H20090307_ctd.nc": "Shared with A09 AND A09.5, but section_id = [A095], labeled as A10",
    "740H20180228_ctd.nc": "Shared with A09 AND A09.5, but section_id = [A09.5-245], labeled as A10",
    "None_ctd.nc": "Unique but section_id was wrong",
    "06AQ19941123_ctd.nc": "Shared with A23, but section_id was wrong, labeled as A12",
    "06AQ20060825_ctd.nc": "Shared with A21, but section_id was wrong, labeled as A12",
    "316N19840111_ctd.nc": "A13.5, but section_id = [AJAX], qc = 1 = uncalibrated",
    "316N19831007_ctd.nc": "A13.5, but section_id = [AJAX], qc = 1 = uncalibrated",
    "35A3CITHER3_2_ctd.nc": "A13.5, but section_id = [AJAX]",
    "3175MB93_ctd.nc": "Shared with AR21, but section_id = [AR21b], labeled as A16",
    "74JC10_1_ctd.nc": "Shared with A23, but section_id = [A23], labeled as A16",
    "74DI233_ctd.nc": "Shared with AR21, but section_id = [AR21], labeled as A16",
    "74JC19990315_ctd.nc": "Shared with A23 and ALBATROSS, but section_id = [ALBATROSS], labeled as A16, qc = 0 = not assigned",
    "09FA20000926_ctd.nc": "Shared with I05, I10 and ISSO3, but section_id = [I02], labeled as I05",
    "33RR20180918_ctd.nc": "P16, but section_id was wrong",
    "325020131025_ctd.nc": "P21, but section_id was wrong",
    "74DI200_1_ctd.nc": "S04, but section_id was wrong",
    "09A9604_1_ctd.nc": "Contains SO4, but section_id = [AURORA96, SR03], labeled as SR03",
    "490S20181205_ctd.nc": "S04, but section_id was wrong",
    "490S20190121_ctd.nc": "S04, but section_id was wrong",
    "09AR9309_1_ctd.nc": "SR03, but section_id was wrong",
    "09AR9407_1_ctd.nc": "SR03, but section_id was wrong",
    "35PK20140515_ctd.nc": "Shared with A25 AND OVIDE, but it has no section_id, labeled as A01",
    "06AQ20080210_ctd.nc": "Does not contain the section_id variable",
    "35MF20080207_ctd.nc": "Does not contain the section_id variable",
    "33RO20230306_ctd.nc": "qc = 1 = uncalibrated",
    "33RO20230413_ctd.nc": "qc = 1 = uncalibrated"
}

# Creating a dictionary with the new names for the wrong sections_id
# actual id : real id
section_rename = {
    "I5" : "I05",
    "I9S" : "I09S",
    "P1W" : "P01W",
    "P1C" : "P01C",
    "S4" : "S04",
    "SR04" : "S04",
    "S4P" : "S04"
}


def homogenize_section_id(
        ds : xr.core.dataset.Dataset,
        section_rename : dict
) -> xr.core.dataset.Dataset:
    """
    Change the name of wrong section_id to the correct one

    :param dataset: xarray dataset
    :param section_rename: dictionary with the new names for the wrong sections_id
    :return dataset: xarray dataset with homogenized section_id
    """
    for i in range(len(ds["section_id"].values)):
        k = 0
        new_name = section_rename.get(ds["section_id"].values[i])
        if new_name is not None:
            k += 1
            ds["section_id"].values[i] = new_name
            if k == 1:
                print("Homogeneizado")
        else:
            continue
    return ds


def vars_coords_interest(
        dataset : xr.core.dataset.Dataset,
        excluded_vars : list = []
) -> tuple:
    """
    Exclude the unnecessary or not wanted variables

    :param dataset: xarray dataset
    :param excluded_vars: list containing strings indicating which classes must be excluded
    :return vars_interest: list with variables of interest
    """
    data_vars = dataset.data_vars
    vars_interest = [var for var in data_vars 
                     if "_qc" not in var and 
                     "_error" not in var and 
                     var not in excluded_vars]
    coords_interest = [coord for coord in dataset.coords
                       if "_qc" not in coord and
                       "_error" not in coord]
    
    qcs = [var for var in data_vars
           if "_qc" in var]
    
    return (vars_interest, coords_interest, qcs)
            

def get_years(
        file_path : str
) -> list:
    """
    Obtain the number of the years when samples were taken

    :param file_path: path of the file
    :return: list or int with the number of years
    """
    ds = xr.load_dataset(filename_or_obj = file_path)
    years = []
    try:
        assert "time" in ds.coords
    except AssertionError:
        return "NO_YEAR_REGISTERED"

    for date in ds.time.values: 
        if str(date)[:4] not in years:
            years.append(str(date)[:4])
    
    return years if len(years) > 1 else years[0]
    

def save_fmt(
        path : str
) -> None:
    """
    Saves a .csv with columns Fichero, Sección, Año, Ref

    :param path: directory
    """
    with open(f"./Data/data.csv", "w") as f:
        f.write(f"File,Section,Year,Ref,Comment\n")
        for section in sorted(os.listdir(path)):
            print(path+section)
            for file_ in glob.glob(path + "/" + section + "/*.nc"):
                f_path = file_
                ds = xr.load_dataset(f_path)
                attrs = ds.attrs
                if "correction_comment" in attrs:
                    years = get_years(f_path)
                    ds = xr.load_dataset(f_path)
                    exist_ctd = "ctd_temperature" in ds.data_vars
                    vars_, coords, qcs = vars_coords_interest(ds)
                    if type(years) == list:
                        for i in range(len(years)):
                            f.write(f"{file_},{section},{years[i]},{str(ds.ctd_temperature.reference_scale) if exist_ctd else str(0)},\"{attrs['correction_comment']}\" \n")
                    else:
                        f.write(f"{file_},{section},{years},{str(ds.ctd_temperature.reference_scale) if exist_ctd else str(0)},\"{attrs['correction_comment']}\" \n")
                #print(file_)
                try:
                    assert f_path.endswith(".nc")
                    years = get_years(f_path)
                    ds = xr.load_dataset(f_path)
                    exist_ctd = "ctd_temperature" in ds.data_vars
                    vars_, coords, qcs = vars_coords_interest(ds)
                    if type(years) == list:
                        for i in range(len(years)):
                            f.write(f"{file_},{section},{years[i]},{str(ds.ctd_temperature.reference_scale) if exist_ctd else str(0)}, 0 \n")
                    else:
                        f.write(f"{file_},{section},{years},{str(ds.ctd_temperature.reference_scale) if exist_ctd else str(0)}, 0 \n")
                except AssertionError:
                        continue

def correct_sections(
        src_path : str,
        dst_path : str,
        start_section : str = "A01",
        end_section : str = None
) -> None:
    """
    Give a NaN value for variables which doesnt correspond to the desired section id

    :param src_path: source directory
    :param dst_path: destination directory
    """
    sections = sorted(os.listdir(src_path))
    print(sections)
    index_start = sections.index(start_section)
    index_end = sections.index(end_section) if end_section is not None else None
    for section in sections[index_start:index_end] if end_section is not None else sections[index_start:]:
        print(f"Correcting {section}....")
        for f in os.listdir(src_path + section + "/"):
            f_path = src_path + section + "/" + f
            if f_path.endswith('.nc'):
                print(f"Correcting {f}....")
                if f in comments:
                    comentario = comments.get(f)
                    ds = xr.load_dataset(f_path)
                    vars_, coords, qcs = vars_coords_interest(dataset = ds)

                    ds = ds.where(np.isnan(ds.latitude) == False).where(np.isnan(ds.longitude) == False)
                            
                                
                    for salinity in ["ctd_salinity", "ctd_salinity_unk", "ctd_salinity_68"]:
                        if salinity in vars_:
                            sal = salinity
                    ds = ds.where(ds[sal] >= 30).where(ds[sal] <= 40)

                    if "ctd_temperature_68" in vars_ and "ctd_temperature" in vars_:
                        print("ctd_temperature_68 and ctd_temperature in vars_")
                        ds = ds.drop_vars(["ctd_temperature_68", "ctd_temperature_68_qc"])
                    elif "ctd_temperature_68" in vars_ and "ctd_temperature" not in vars_:
                        print("ctd_temperature_68 in vars_")
                        atributos = ds["ctd_temperature_68"].attrs
                        ds["ctd_temperature_68"] = ds["ctd_temperature_68"] / 1.00024
                        ds["ctd_temperature_68"].attrs = atributos
                        ds = ds.rename({"ctd_temperature_68" : "ctd_temperature",
                                        "ctd_temperature_68_qc" : "ctd_temperature_qc"})
                    elif "ctd_temperature_68" not in vars_ and "ctd_temperature" in vars_:
                        print("ctd_temperature in vars_")

                    vars_, coords, qcs = vars_coords_interest(dataset = ds)
                    for qc in qcs:
                        if "ctd_temperature" in qc or "ctd_salinity" in qc:
                            if 2 in np.unique(ds[qc].values):
                                ds = ds.where(ds[qc] == 2)
                            elif 1 in np.unique(ds[qc].values) and 2 not in np.unique(ds[qc].values):
                                ds = ds.where(ds[qc] == 1)


                    ds["section_id"] = section # Añadimos section_id y ponemos misma sección
                    ds.attrs["correction_comment"] = comentario # Añadimos el comentario en los artibutos

                    if os.path.exists(dst_path + section + "/") == False: os.mkdir(dst_path + section + "/")
                    years = get_years(f_path)
                    if type(years) != list:
                        ds.to_netcdf(dst_path + section + "/" + years + "_" + f)
                    else:
                        years_ = ""
                        for year in years:
                            years_ += year + "_"
                        ds.to_netcdf(dst_path + section + "/" + years_ + f)
                    ds.close()
                
                else:    
                    ds = xr.load_dataset(f_path)
                    ds = ds.set_coords("section_id")
                    ds = homogenize_section_id(ds, section_rename)
                    vars_, coords, qcs = vars_coords_interest(dataset = ds)
                            
                    for i in range(len(ds["section_id"].values)):
                        if section not in ds["section_id"].values[i]:
                            ds["latitude"].values[i] = np.nan
                            ds["longitude"].values[i] = np.nan
                            

                    ds = ds.where(np.isnan(ds.latitude) == False).where(np.isnan(ds.longitude) == False)
                    
                
                    for salinity in ["ctd_salinity", "ctd_salinity_unk", "ctd_salinity_68"]:
                        if salinity in vars_:
                            sal = salinity
                    ds = ds.where(ds[sal] >= 30).where(ds[sal] <= 40)

                    if "ctd_temperature_68" in vars_ and "ctd_temperature" in vars_:
                        print("ctd_temperature_68 and ctd_temperature in vars_")
                        ds = ds.drop_vars(["ctd_temperature_68", "ctd_temperature_68_qc"])
                    elif "ctd_temperature_68" in vars_ and "ctd_temperature" not in vars_:
                        print("ctd_temperature_68 in vars_")
                        atributos = ds["ctd_temperature_68"].attrs
                        ds["ctd_temperature_68"] = ds["ctd_temperature_68"] / 1.00024
                        ds["ctd_temperature_68"].attrs = atributos
                        ds = ds.rename({"ctd_temperature_68" : "ctd_temperature",
                                        "ctd_temperature_68_qc" : "ctd_temperature_qc"})
                    elif "ctd_temperature_68" not in vars_ and "ctd_temperature" in vars_:
                        print("ctd_temperature in vars_")

                    vars_, coords, qcs = vars_coords_interest(dataset = ds)
                    for qc in qcs:
                        if "ctd_temperature" in qc or "ctd_salinity" in qc:
                            if 2 in np.unique(ds[qc].values):
                                ds = ds.where(ds[qc] == 2)
                            elif 1 in np.unique(ds[qc].values) and 2 not in np.unique(ds[qc].values):
                                ds = ds.where(ds[qc] == 1)

                
                    if os.path.exists(dst_path + section + "/") == False: os.mkdir(dst_path + section + "/")
                    years = get_years(f_path)
                    if type(years) != list:
                        ds.to_netcdf(dst_path + section + "/" + years + "_" + f)
                    else:
                        years_ = ""
                        for year in years:
                            years_ += year + "_"
                        ds.to_netcdf(dst_path + section + "/" + years_ + f)
                        
                    ds.close()
            print("Done!\n")



if __name__ == "__main__":

    correct_sections(src_path = "./Data/direct_downloads/",dst_path = "./Data/corrected_sections/")
    #save_fmt('./Data/corrected_sections')

    
            
    
    
    
