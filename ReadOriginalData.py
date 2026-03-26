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
        f.write(f"Fichero,Sección,Año,Ref,qcs\n")
        for section in sorted(os.listdir(path)):
            print(path+section)
            for file_ in glob.glob(path + "/" + section + "/*.nc"):
                f_path = file_
                #print(file_)
                try:
                    assert f_path.endswith(".nc")
                    years = get_years(f_path)
                    ds = xr.load_dataset(f_path)
                    exist_ctd = "ctd_temperature" in ds.data_vars
                    vars_, coords, qcs = vars_coords_interest(ds)
                    if type(years) == list:
                        for i in range(len(years)):
                            f.write(f"{file_}, {section}, {years[i]}, {str(ds.ctd_temperature.reference_scale) if exist_ctd else str(0)} \n")
                    else:
                        f.write(f"{file_}, {section}, {years}, {str(ds.ctd_temperature.reference_scale) if exist_ctd else str(0)} \n")
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
                print(f"Correcting {section}....")
                if f_path.endswith('.nc'):
                    ds = xr.open_dataset(f_path)
                    vars_, coords, qcs = vars_coords_interest(dataset = ds)
        
                    try:
                       assert "section_id" in ds.data_vars
                    except AssertionError:
                        continue
                
                    for i in range(len(ds["section_id"])):
                        if section not in ds["section_id"].values[i]:
                            ds.longitude[i] = np.nan
                            ds.latitude[i] = np.nan

                    ds = ds.where(np.isnan(ds.latitude) == False).where(np.isnan(ds.longitude) == False)
                    for qc in qcs:
                        if "temperature" in qc:
                            ds = ds.where(ds[qc] == 2)
                
                    for salinity in ["ctd_salinity", "ctd_salinity_unk", "ctd_salinity_filt", "ctd_salinity_68"]:
                        if salinity in vars_:
                            sal = salinity
                
                    ds = ds.where(ds[sal] >= 30).where(ds[sal] <= 40)
                    if "ctd_temperature_68" in vars_:
                        ds["ctd_temperature_68"] = ds["ctd_temperature_68"] / 1.00024
                
                    if os.path.exists(dst_path + section + "/") == False: os.mkdir(dst_path + section + "/")
                    years = get_years(f_path)
                    if type(years) != list:
                        ds.to_netcdf(dst_path + section + "/" + years + "_" + f)
                    else:
                        years_ = ""
                        for year in years:
                            years_ += year + "_"
                            ds.to_netcdf(dst_path + section + "/" + years_ + f)
            print("Done!\n")


secs_interest = [
        "A01",
        "A05",
        "A02",
        "A10",
        "A12",
        "A13.5",
        "A16",
        "A20",
        "A22",
        "I03",
        "I04",
        "I05",
        "I06",
        "I08",
        "I09",
        "I08/I09"
        "I09S",
        "P01",
        "P02",
        "P03",
        "P06",
        "P10",
        "P14",
        "P15",
        "P16",
        "P17",
        "P18",
        "P21",
        "SR03",
        "S04"        
    ]

if __name__ == "__main__":

    correct_sections(src_path = "./Data/direct_downloads/",dst_path = "./Data/corrected_sections/")
    save_fmt('./Data/corrected_sections')

    
            
    
    
    
