from ReadOriginalData import *

def plot_ocean(
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
    fig = plt.figure(figsize = (12, 10))
    ax = plt.axes(projection = projection(central_long))
    ax.set_extent((-180, 180, -90, 90))
    ax.coastlines()
    ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.4, linestyle='--')
    print("Empezando")
    for i, section in enumerate(sorted(os.listdir(path))):
            for j, f in enumerate(os.listdir(path + section + "/")):
                if f[-3:] == ".nc":
                    print(f"Plotting section {section} of file {f}...")
                    ds = xr.load_dataset(filename_or_obj = path + section + "/" + f)
                    ax.scatter(ds.longitude, ds.latitude, marker = ".", color = "k", transform = projection())
                else:
                    continue
    

    plt.title(f"Sections of oceans")
    plt.tight_layout()

    if dst_path is not None:
        print("Guardando...")
        plt.savefig(dst_path + "oceans_sections.png")
        print("Done")

if __name__ == "__main__":
    plot_ocean(path = "./Data/corrected_sections/", projection = ccrs.PlateCarree, central_long = 0, dst_path = "./plots/")