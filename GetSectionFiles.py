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
from ReadOriginalData import *


def get_section_files(
        path : str,
        sections : list
) -> tuple:
    """
    Save the names of the files of WOCE sections

    :param path: str with directory of files
    :param sections: list with sections of interest
    :return sections_files: tuple containing list of ids and file names
    """
    section_ids = []
    files_with_sect = []
    years = []
    for f in tqdm(os.listdir(path), desc = "Filtering for sections...", total = len(os.listdir(path))):
        try:
            assert os.path.exists(path+f)
        except AssertionError:
            continue
        ds = xr.load_dataset(filename_or_obj = path + f)
        try:
            assert "section_id" in ds.data_vars
        except AssertionError:
            continue
        
        section = ds["section_id"].values
        for id_ in sections:
            if id_ in str(section):
                if os.path.exists(f"sections/{id_}/") == False : os.mkdir(f"sections/{id_}/")  
                os.system(f"cp {path}{f} sections/{id_}/{f}")
                section_ids.append(id_)
                files_with_sect.append(f)
                years.append(get_years(f"sections/{id_}/{f}"))
                
    return (section_ids, files_with_sect, years)
