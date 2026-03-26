from ReadOriginalData import *
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
            nombre = f.split(".")[0]
            if f_path.endswith('.nc'):
                ds = xr.load_dataset(filename_or_obj = f_path)
                fig = plt.figure(figsize = (12, 10))
                ax = plt.axes(projection = projection(central_longitude = 180 if str(section[0]) == "I" or str(section[0]) == "P" else 0))
                ax.set_extent((-180, 180, -90, 90))
                ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.4, linestyle='--')
                ax.coastlines()
                ax.scatter(ds.longitude, ds.latitude, marker = ".", color = colors[i], label = f"{f}", transform = projection())
                # if copy == True: os.system(f"cp {path}{section}/{f} {save_path}{f}")
                plt.title(f"Section {section} {nombre}" )
                plt.legend()
                plt.savefig(f"{save_path}section_{section}_{nombre}.png")
                plt.close(fig = fig)
        print("Done!")

if __name__ == "__main__":
    plot_all_sections("Data/corrected_sections/", "plots/", projection = ccrs.PlateCarree, copy = True)