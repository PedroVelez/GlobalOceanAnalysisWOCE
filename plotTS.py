from ReadOriginalData import *


def download_sst(
        dst_path : str,
        year : int = None
) -> None:
    """
    Use FTP to download SST of given year from NOAA

    :param dst_path: destination path
    :param year: year of sample, actual year if None
    """
    actual_year = datetime.date.today().year if year == None else year
    file_ = f"sst.day.mean.{actual_year}.nc"
    os.chdir(dst_path)
    ftp = FTP("ftp.cdc.noaa.gov")
    ftp.login()
    ftp.cwd("Datasets/noaa.oisst.v2.highres/")
    print(f"Downloading {file_} at {dst_path}.....")
    ftp.retrbinary("RETR " + file_, open(file_, "wb").write)
    ftp.quit()


def plot_sst(
        file_path : str,
        time : str,
        projection : ccrs.Projection,
        central_long : float
) -> None:
    """
    Plot SST using cartopy given a certain projection of axes and a year

    :param file_path: path of the .nc file
    :param time: YYYY-MM-DD format
    :param projection: cartopy projection
    :param central_long: central longitude of the projection
    """
    ds = xr.load_dataset(filename_or_obj = file_path)
    sst = ds.sst.sel(time = time, method = "nearest")

    fig = plt.figure(figsize = (12, 10))
    ax = plt.axes(projection = projection(central_longitude = central_long))
    ax.set_extent((-180, 180, -90, 90))
    ax.coastlines()
    ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.4, linestyle='--')
    sst.plot(ax = ax, transform = projection(), cmap = "hot")
    plt.show()


def plot_section(
        ds : xr.Dataset,
        projection : ccrs.Projection,
        central_long : float,
        color : str
) -> None:
    """
    Plot section given a file path

    :param file_path: path of the .nc file
    :param projection: cartopy projection
    :param centrla long: central longitude of the projection
    :param color: color of the section
    """
    lat_str = ""
    lon_str = ""
    for lat, lon in zip(["latitude", "lat"], ["longitude", "lon"]):
        if lat in ds.coords and lon in ds.coords:
            lan_str = lat
            lon_str = lon
    fig = plt.figure(figsize = (12, 10))
    ax = plt.axes(projection = projection(central_longitude = central_long))
    ax.set_extent((-180, 180, -90, 90))
    ax.coastlines()
    ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.4, linestyle='--')
    ax.scatter(ds[lon_str], ds[lat_str], marker = ".", color = color, transform = projection())


def plot_all_sections(
    path : str,
    dst_path : str,
    projection : ccrs.Projection,
    central_long : float = 0,
    copy : bool = False,
    start_section : str = "A01"
) -> None:
    """
    Plot all the sections of a given directory

    :param path: directory
    :param dst_path: directory for figures to be saved
    :param projection: cartopy projection
    :param central_long: central longitude of the projection
    :param copy: boolean to indicate if files are copied to dst_path
    :param start_secction: section str where user wants to start, default -> A01
    """
    colors = ["b", "g", "r", "c", "m", "y", "k", "peru", "lime", "slategrey", "yellowgreen", "hotpink","b", "g", "r", "c", "m", "y", "k", "peru", "lime", "slategrey", "yellowgreen", "hotpink"]
    sections = sorted(os.listdir(path))
    index_start = sections.index(start_section)
    for section in sections[index_start:]:
        print(f"Plotting section {section}....")
        save_path = f"{dst_path}{section}/"
        if os.path.exists(save_path) == False: os.mkdir(save_path)
        for i, f in enumerate(os.listdir(path + section + "/")):
            f_path = path + section + "/" + f
            if f_path.endswith('.nc'):
                ds = xr.load_dataset(filename_or_obj = f_path)
                fig = plt.figure(figsize = (12, 10))
                ax = plt.axes(projection = projection(central_longitude = 180 if str(section[0]) == "I" or str(section[0]) == "P" else 0))
                ax.set_extent((-180, 180, -90, 90))
                ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.4, linestyle='--')
                ax.coastlines()
                ax.scatter(ds.longitude, ds.latitude, marker = ".", color = colors[i], label = f"{f}", transform = projection())
                #if copy == True: os.system(f"cp {path}{section}/{f} {save_path}{f}")
                plt.title(f"Section {section}")
                plt.legend()
                plt.savefig(f"{save_path}section_{section}.png")
                plt.close(fig = fig)
        print("Done!")


def plot_ocean(
        ocean : str,
        path : str,
        projection : ccrs.Projection,
        central_long : float,
        dst_path : str = None
) -> None:
    """
    Plot all sections of given ocean

    :param ocean: first letter of the ocean's name
    :param path: directory
    :param projection: cartopy projection
    :param central_long: central longitude of the projection
    :param dst_path: directory for figures to be saved
    """
    colors = ["b", "g", "r", "c", "m", "y", "k", "peru", "lime", "slategrey", "yellowgreen", "hotpink"]
    fig = plt.figure(figsize = (12, 10))
    ax = plt.axes(projection = projection(central_longitude = central_long))
    ax.set_extent((-180, 180, -90, 90))
    ax.coastlines()
    ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.4, linestyle='--')
    for i, section in enumerate(sorted(os.listdir(path))):
        if section[0] == ocean:
            for j, f in enumerate(os.listdir(path + section + "/")):
                ds = xr.load_dataset(filename_or_obj = path + section + "/" + f)
                ax.scatter(ds.longitude, ds.latitude, marker = ".", color = colors[i], label = f"{section}" if j == 0 else None, transform = projection())
    
    plt.legend()
    if dst_path is not None:
        if os.path.exists(path = dst_path + "oceans/") == False: os.mkdir(dst_path + "oceans/")
        plt.savefig(dst_path + "oceans/" + ocean)


def plot_variable(
        dir_ : str, 
        variable : str, 
        yincrease : bool = True, 
        traspose : bool = False
) -> None:
    """
    Plot certain variable for all .nc files in dir_

    :param dir_: str of directory
    :param variable: str of variable to plot
    :param yincrease: indicates if y increases or decreases in the plot
    :param traspose: traspose the variable axes if needed
    """
    files = os.listdir(dir_)
    for f in files:
        ds = xr.open_dataset(filename_or_obj= dir_ + f)
        vars_ = ds.data_vars
        try:
            assert variable in vars_, "Variable doesnt exist"
        except AssertionError:
            print(f"Variable {variable.upper()} doesnt exist in {f}")
            continue
        os.mkdir(f"figs/{variable}/") if os.path.exists(f"figs/{variable}/") == False else print(f"{variable} plot of {f} saved at figs/{variable}")
        ds[variable] = ds[variable].T if traspose == True else ds[variable]
        ds[variable].plot(figsize = (10,6), yincrease = yincrease)
        plt.savefig(f"figs/{variable}/{f[:-3]}.pdf")


def TS_plot(
        path : str,
        dst_path : str,
        start_section : str = "A01",
        end_section : str = None,
        raw : bool = False,
        filt : bool = False
) -> None:
    """
    Compute a TS plot and saves it

    :param path: directory
    :param dst_path: directory of figures to be saved
    :param start_secction: section str where user wants to start, default -> A01
    :param raw: boolean to indicate to plot normal plot, or raw to detect anomalies
    """
    print(f"Destination path: {dst_path}")
    directory = os.listdir(path = path)
    fig = plt.figure(figsize = (8, 10))
    colors = ["b", "g", "r", "c", "m", "y", "k", "peru", "lime", "slategrey", "yellowgreen", "hotpink"]
    sections = sorted(os.listdir(path))
    index_start = sections.index(start_section)
    index_end = sections.index(end_section) if end_section is not None else None
    for section in sections[index_start:index_end] if end_section is not None else sections[index_start:]:
        print(f"Plotting TS diagram of section {section}...." if raw == False else f"Plotting raw TS diagram of section {section}....")

        fig, ax = plt.subplots()
        for i, f in enumerate(sorted(os.listdir(path + section + "/"))):
            try:
                assert f[-3:] == ".nc"
                ds = xr.open_dataset(filename_or_obj = path + section + "/" + f)
                pressure = "pressure" if filt == False else "pressure_interp"
                assert pressure in ds.coords
                t = 0
                

                for temperature, salinity in zip(["ctd_temperature", "ctd_temperature_unk", "ctd_temperature_filt", "ctd_temperature_68"], ["ctd_salinity", "ctd_salinity_unk", "ctd_salinity_filt", "ctd_salinity_68"]):
                    if temperature in ds.data_vars:
                        t = ds[temperature]
                    if salinity in ds.data_vars:
                        sal = salinity
                #ds["SA"] = gsw.SA_from_SP(ds[sal], ds.pressure, ds.longitude, ds.latitude)
                #t = gsw.CT_from_t(ds["SA"], t, ds[pressure])

                for j in range(t.shape[0]):
                    if j == 0:
                        ax.plot(
                            ds[sal][j, :],
                            t[j, :], 
                            f"{colors[i]}", 
                            #label = f"{f}", 
                            marker = ".",
                            markersize=0.4 if raw == False else 1,
                            alpha=0.2 if raw == False else 0.5,
                            linestyle='' if raw == False else "-"
                        )

                    ax.plot(
                        ds[sal][j, :],
                        t[j, :], 
                        f"{colors[i]}", 
                        marker = ".",
                        markersize=0.4 if raw == False else 1,
                        alpha=0.2 if raw == False else 0.5,
                        linestyle='' if raw == False else "-"
                    )
                ds.close()
            except AssertionError:
                a = f"{f} has not a pressure variable" if f[-3:] == ".nc" else f"{f} is not a netCDF file"
                print(f"AssertionError: {a}")
                ds.close()
            
        #save_path = f"{dst_path}{section}/"
        save_path = dst_path
        if os.path.exists(save_path) == False: os.mkdir(save_path)
        ax.set_title(f"Section {section}")
        ax.set_xlabel("Salinity (g / kg)")
        ax.set_ylabel("Temperature (ºC)")
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon = False)
        plt.tight_layout()
        fig.savefig(f"{save_path}TS_{section}.png" if raw == False else f"{save_path}raw_TS_{section}.png")
        plt.close("all")
        print("Done! \n")


def plot_sections_years(
        data : str,
        dst_path : str
) -> None: 
    """
    Plot occupation of sections over years

    :param data: csv file with data (Required "Sección" and "Año" columns)
    :param dst_path" directory for figure to be saved
    """
    df = pd.read_csv(data)
    fig = plt.figure(figsize = (5, 10))
    years = df["Año"][::-1]
    sections = df["Sección"][::-1]
    plt.plot(years, sections, ".k")
    plt.xlabel("Years")
    plt.grid()
    plt.savefig(f"{dst_path}occupation.png")
    plt.close()


if __name__ == "__main__":
    #plot_sections_years("corrected_sections/", "plots/")
    #plot_all_sections("corrected_sections/", "plots/", projection = ccrs.PlateCarree, copy = True)
    #TS_plot(path = "./corrected_sections/", dst_path = "./plots/", raw = True)
    plot_sections_years(data = "./Data/data.csv", dst_path = "./Data/")