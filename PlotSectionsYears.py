# Import the same packages as ReadOriginalData.py
from ReadOriginalData import *


# Define a function to plot the occupation of sections over years
def plot_sections_years(
        data : str,
        dst_path : str
) -> None: 
    """
    Plot occupation of sections over years

    :param data: csv file with data (Required "Sección" and "Año" columns)
    :param dst_path" directory for figure to be saved
    """

    # Open csv file
    df = pd.read_csv(data, quotechar='"')

    # Create figure
    fig = plt.figure(figsize = (5, 10))

    # Get years and sections
    years = df["Year"][::-1]
    sections = df["Section"][::-1]

    # Plot
    plt.plot(years, sections, ".k")

    # Add features
    plt.xlabel("Years")
    plt.grid()

    # Save the figure
    plt.savefig(f"{dst_path}occupation.png")

    # Close the figure
    plt.close()

if __name__ == "__main__":
    plot_sections_years(data = "./Data/data.csv", dst_path = "./plots/")