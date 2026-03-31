from ReadOriginalData import *

def plot_sections_years(
        data : str,
        dst_path : str
) -> None: 
    """
    Plot occupation of sections over years

    :param data: csv file with data (Required "Sección" and "Año" columns)
    :param dst_path" directory for figure to be saved
    """
    df = pd.read_csv(data, quotechar='"')
    fig = plt.figure(figsize = (5, 10))
    years = df["Year"][::-1]
    sections = df["Section"][::-1]
    plt.plot(years, sections, ".k")
    plt.xlabel("Years")
    plt.grid()
    plt.savefig(f"{dst_path}occupation.png")
    plt.close()

if __name__ == "__main__":
    plot_sections_years(data = "./Data/data.csv", dst_path = "./plots/")