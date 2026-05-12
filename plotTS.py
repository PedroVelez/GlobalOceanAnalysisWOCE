# Import the same packages as ReadOriginalData.py
from ReadOriginalData import *

# Define a function to compute and save TS diagram
def TS_plot(
        path : str,
        dst_path : str,
        start_section : str = "A01",
        end_section : str = None,
        raw : bool = False
) -> None:
    """
    Compute a TS plot and saves it

    :param path: directory
    :param dst_path: directory of figures to be saved
    :param start_secction: section str where user wants to start, default -> A01
    :param raw: boolean to indicate to plot normal plot, or raw to detect anomalies
    """

    directory = os.listdir(path = path) # Get the directory
    sections = sorted(os.listdir(path)) # Sorted sections

    # Define the start and end section
    index_start = sections.index(start_section)
    index_end = sections.index(end_section) if end_section is not None else None

    # Iterate for every section
    for section in sections[index_start:index_end] if end_section is not None else sections[index_start:]:
        print(f"Plotting TS diagram of section {section}...." if raw == False else f"Plotting raw TS diagram of section {section}....")

        # Iterate for every file
        for f in sorted(os.listdir(path + section + "/")):
            try:
                assert f[-3:] == ".nc"
                print(f"file: {f}")
                fig, ax = plt.subplots()
                ds = xr.open_dataset(path + section + "/" + f)
                t = 0

                # Get the temperature and salinity  
                for temperature, salinity in zip(["ctd_temperature", "ctd_temperature_unk"], ["ctd_salinity", "ctd_salinity_unk", "ctd_salinity_68"]):
                    if temperature in ds.data_vars and t == 0:
                        t = ds[temperature]
                    if salinity in ds.data_vars:
                        sal = ds[salinity]

                # Plot the TS diagram
                plt.scatter(sal, t,
                         s = 0.4 if raw == False else 1, 
                         alpha = 0.2 if raw == False else 0.5,
                        )

                ds.close()
                
                # Save the plot
                save_path = f"{dst_path}{section}/"
                if os.path.exists(save_path) == False: os.mkdir(save_path)
                ax.set_title(f"Section {section} TS diagram for {f.split('.')[0]}")
                ax.set_xlabel("Salinity (g / kg)")
                ax.set_ylabel("Temperature (ºC)")
                plt.tight_layout()
                fig.savefig(f"{save_path}TS_{f.split('.')[0]}.png" if raw == False else f"{save_path}raw_TS_{f.split('.')[0]}.png")
                plt.close("all")
                print("Done! \n")
            except AssertionError:
                a = f"{f} has not a pressure variable" if f[-3:] == ".nc" else f"{f} is not a netCDF file"
                print(f"AssertionError: {a}")
                
            
        





if __name__ == "__main__":
    TS_plot(path = "./Data/corrected_sections/", dst_path = "./plots/", raw = True)