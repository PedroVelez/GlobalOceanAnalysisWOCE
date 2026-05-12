# Import the same packages as ReadOriginalData.py
from ReadOriginalData import *

# Define a function for plot all sections in the same figure
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

    # Create figure
    fig = plt.figure(figsize = (12, 10))
    ax = plt.axes(projection = projection(central_long))

    # Add features
    ax.set_extent((-180, 180, -90, 90))
    ax.coastlines()
    ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.4, linestyle='--')
    print("Empezando")

    # Iterate for every file
    for i, section in enumerate(sorted(os.listdir(path))):
            for j, f in enumerate(os.listdir(path + section + "/")):
                if f[-3:] == ".nc":
                    print(f"Plotting section {section} of file {f}...")
                    # Open file
                    ds = xr.load_dataset(filename_or_obj = path + section + "/" + f)

                    # Plot
                    ax.scatter(ds.longitude, ds.latitude, marker = ".", color = "k", transform = projection())
                    
                    # Close file
                    ds.close()
                    
                else:
                    continue
    

    plt.title(f"Sections of oceans")
    plt.tight_layout()
    
    # Save the figure
    if dst_path is not None:
        print("Guardando...")
        plt.savefig(dst_path + "oceans_sections.png")
        print("Done")
    
    # Close the figure
    plt.close()

if __name__ == "__main__":
    plot_ocean(path = "./Data/corrected_sections/", projection = ccrs.PlateCarree, central_long = 0, dst_path = "./plots/")