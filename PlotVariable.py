from ReadOriginalData import *


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
