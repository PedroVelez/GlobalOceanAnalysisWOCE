## Identify the section of the raw data

**GetSectionFiles.py** analyzes the `./Data/direct_downloads` folder when the downloaded files have not yet been organized by section. It returns a list of files and their associated sections, when available, since some files do not contain a `section_id`.

**SectionExtractor.ipynb** reads the files in `./Data/direct_downloads` and extracts the `section_id` variable from each file, making it possible to identify inconsistencies. This ensures that all potential issues that could lead to data loss during processing are detected.

## Datos nuevos

En el fichero DatosNuevos2026.txt, se encuentran los archivos descargados que fueron añadidos en marzo de 2026.

**NewDataComparison.ipynb**, se encuentran dos pequeñas celdas que imprimen el nombre del archivo, el expocode, la fecha de inicio y la de final de la carpeta Data/direct_downloads/ y Data/direct_downloadas_nuevos/ de una misma sección, de forma que se puede comprobar si los ficheros etiquetados como nuevos realmente pertenecen a una campaña nueva.

## Identificar valores qc para posterior filtrado

**QualityControlExtractor.ipynb** usa los datos de Data/direct_downloads/ y crea una lista por secciones de las variables que tienen control de calidad y que valores tienen estos. Sabiendo los distintos valores de control de calidad que tienen las variables en los archivos, se puede escoger un filtrado más apropiado. Se recomienda revisar la documentación: [WOCE CTD Quality Codes](https://exchange-format.readthedocs.io/en/latest/quality.html)
    

## Leer datos y tabla

En ./Data/direct_downloads/, están las las descargas crudas de internet ya organizadas por secciones WOCE. Cuando una campaña tenia 'section_id' y se realizaba de manera conjunta en dos o más secciones WOCE se copiaba por duplicado en las carpetas de las secciones. Cuando un campaña no tiene 'section_id' se copia solamente en una carpeta, la que más se asemeja a la sección correspondiente.

**ReadOriginalData.py** contiene la función correct_sections() que 'corrige' las secciones. Está función emplea la variable 'section_id' (cuando existe) de los archivos netcdf para su clasificación por secciones. Los valores de latitud y longitud que no pertenezcan a secciones de interés son recortados, dejando únicamente los datos de secciones puras. Con respecto a las variables aplica un filtro de control de calidad con etiqueta 2 (Buenas calidad) y en su defecto 1 (Sin calibrar) o 0 (no asociado) para usar solo medidas eficientes. Además, de entre todos los posibles nombres de salinidad, se queda con el que corresponde y recorta para que los datos de salinidad estén solo entre 30 y 40 en sus respectivas unidades. Si existe la variable 'ctd_temperature-68' la convierte a grados celsius dividiendo entre 1.00024.

También extrae los años de muestreo del archivo y los usa para modificar los nombres de los ficheros de secciones en la carpeta ./Data/corrected_sections/. También crea un fichero data.csv con nombres de los ficheros, su sección, año y referencia.  En la versión del 27/03/2026, se añade un diccionario con ficheros que tienen algún problema y su respectivo comentario de información, y otro diccionario que indica que distintos nombres puede tener una misma sección. 

Es importante tener en cuenta que si se descargan nuevos datos hay que revisar sus section_id con Section_Extrator.ipynb, para ver si alguno de los nuevos archivos presenta una peculiaridad y en su caso, añadir esta peculiaridad al correspondiente diccionario que se encuentra al principio del archivo ReadOriginalData.py.

## Mapa de secciones y ocupaciones

**PlotAllSectionsTracks.ipynb** lee de ./Data/corrected_sections/  y representa la sección que recorre cada archivo en el mapa una por una con el nombre de su sección y el del archivo, guardándolo en ./Data/corrected_sections_plots/'SECTION'. Esta es útil para saber que datos están almacenados de cada archivo.

**PlotOcean.ipynb** lee de ./Data/corrected_sections/ y representa la sección que recorre cada archivo en el mapa, todas en un mismo mapa, de forma que se puede ver las zonas de las que se tienen dados. Guarda el mapa pintado en ./Data/oceanSections.png

**PlotOcupations.ipynb** dibuja la gráfica de **ocupaciones** a partir de ./Data/data.csv, extrayendo el año y la sección de forma que se generá una gráfica de puntos. La gráfica obtenida se guarda en ./Data/ bajo el nombre oceanOcupations.png


## Diagramas TS

**plotTS.py** lee los datos de Data/corrected_sections/ y hace un diagrama TS para cada archivo, guardándolo en ./plots/'SECTION' donde section es la sección que le corresponde.  Contiene el parámetro raw, que si se le da el valor 'FALSE' representa de forma ordinaria, ajustando los ejes, y si se le da el valor 'TRUE' representa sin ajuste automatica, de forma que es más sencillo identificar anomálias, es un parámetro ligado al tamaño de los puntos. Los diagramas se guardan con nombre "raw_TS_NOMBRE_DEL_FICHERO_EN_LA_CARPETA_DE_ENTRADA" si raw = 'TRUE' o igual pero sin el raw en caso de raw = 'FALSE'. También da la opción de indicar que secciones representar, por lo que en caso de solo necesitar representar una única sección, no hay que repetir las demás. Existe una version ipynb.

## Aplica filtro

**AplicaFiltroHanning.ipynb** lee los datos de Data/corrected_sections/, que ya han sido procesados con ReadOriginalData.py y le aplica un filtro Hanning a las variables de interes. Limpia el archivo para que solo tenga las variables y coordenadas necesarias, ya con el filtro aplicado. Devuelve estos ficheros corregidos en la carpeta Data/corrected_sections_filtrado/ en su correspondiente sección. En el notebook se puede ejecutar una prueba previa con la sección A01, además permite escoger la resolución de los puntos del filtrado. 

El procedimiento consiste en crear la curva del filtro hanning para luego hacer una convolución con la variable de interes de forma que está se ajusta a la curva y suaviza los perfiles. Por defecto se usa un filtro con 40 dbar como ancho de kernel y una resolución espacial de 1 m.

## Unir sections

**UneCruises.ipynb** Une todas los datos en una matriz. Lee los datos de Data/corrected_sections_filtrado/, a los que ya se les ha aplicado el filtro Hanning. Guarda en Data/join/ un fichero .nc que contiene todos los datos de todos los archivos. Las variables de este fichero son Temperatura, salinidad, y oxígeno filtrados, además de las densidades y capacidades calorificas a presión constante calculadas. Como coordenas tiene latitud, longitud, fecha y nombre del fichero de origen. Por último como dimensiones tiene N_PROFxN_LEVELS donde N_PROF es la suma de todos los perfiles que habían en los ficheros y N_LEVES va desde 0 hasta el máximo de presión interpolada.
    

## Crear división por cuencas

En la carpeta CreaCuencas hay varios códigos en matlab que crean archivos csv, indicando el valor de la máscara para cada pixel del mapa. La división por cuencas usada se extrae de el artículo de Sarah G.Purkey: [Warming of Global Abyssal and Deep Southern Ocean Waters between the 1990s and 2000s: Contributions to Global Heat Content and Sea Level Rise Budgets](https://journals.ametsoc.org/view/journals/clim/23/23/2010jcli3682.1.xml?tab_body=pdf)

**CreateMask.ipynb** crea dicha máscara devolviendo un archivo netcdf en Data/Mascara/mascara.nc, que contiene el valor de cuenca asociado a cada pixel y el nombre

## Calcula Matriz de ocupaciones

**GridOccupation.ipynb** lee los datos de Data/join/total_filt.nc y devuelve un archivo con el nombre occupation.nc en la carpeta Data/grid/. 
La idea es crear un grid de latitudes y longitudes de resolución ajustable, de forma que para cada pixel del mapa se pueda ver el número de ocupaciones para ese punto, y además que perfiles del archivo total_filt.nc son los que contiene. De esta forma las dimensiones son de $latitud \times longitud \times n_{prof}$, donde $n_{prof}$ es el número máximo de ocupaciones que se esperan para cualquier pixel, es decir, cada punto tendrá un n inferior a $n_{prof}$. 
También tiene unas celdas que añaden una las variables mask y basin (nombre de cuenca) que corresponden a la máscara creada en CreaCuencas/CreateMask.ipynb, de forma que la máscara está ya guardada en los ficheros con el nombre de cada cuenca. Por último, también proporciona los datos de batimetría y la superficie de cada pixel en $m^2$. 
Este mismo notebook también representa las ocupaciones por cada punto del grid en un mapa y una barra de color, de forma que se puede ver el número de perfiles por punto. Las figuras que se obtienen se guardan en /plots/Occupation_grids/ con un nombre de archivo distinto según la resolución usada.  

*Las versiones anteriores de está parte se encuentran contenidas en los archivos: grid_2025.ipynb y grid_2025.grid. Estas incluyen un cálculo descartado de temperatura y salinidad medias de cada perfil.*

__Nota__: La función Locate.py es usada en estos script

## Tendencias y mapas

**CalculaTendencias.ipynb* extrae el grid de la resolución deseada de /Data/grid/ y los datos de temperatura y salinidad de /Data/join/total_filt.nc. Con estos archivos calcula la tendencia en los pixeles donde hayan valores suficientes como para calcular la misma. El criterio es que dicho pixel contenga al menos 3 datos de temperatura y que estos tengan una separación temporal de al menos 2.5 años, aunque esto último puede variar si se desea, por ejemplo para 1990-2025 se suele usar 10 años en su lugar. Guarda un fichero del mismo tipo que el grid, pero con la variable tendencia añadida en /Data/tendency/, indicando años en los que se ha filtrado, niveles y resolución. También guarda mapas en /plots/Tendency_grids/ que permiten ver las tendencias en los puntos en los que existen permitiendo ver si los resultados son buenos.

Tras varias pruebas, se decidio añadir una variable que indica si se quiere usar el método de ajuste de Theil Slopes o el ajuste por mínimos cuadrados usual de polyfit. Theil Slopes toma la mediana de las pendientes de todos los pares de puntos, por lo que en algunos casos será más robusta estadísticamente, ya que da la sensación de que ignora datos atípicos. 

Hay unas breves líneas de código que sirven para la representación de puntos de la distribución de puntos de tendencia por cuencas, de forma que se puede ver si estas se agrupan sobre un valor, o por el contrario las desviaciones dan lugar a poca significancia estadística.

**MapasTendencias.ipynb** lee los datos de /Data/tendency/ y calcula la media y desviación de la tendencia por cuencas, de forma que se representan estas variables en un mapa. Este mapa se guarda en plots/Mapas_Tendencias/ indicando los datos necesarios para entender sus características. Permite decidir si representar la media calculada con Theil Slopes o polyfit, además de si se usa la media usual o la mediana para la media por cuencas

### Tendencias por niveles

**CalculaTendenciaNiveles.ipynb** lee los datos de /Data/grid/ y /Data/join/total_filt.nc y calcula la tendencia en los pixeles donde hayan valores suficientes como para calcular la misma. En principio el criterio es que dicho pixel contenga al menos 3 datos de temperatura y que estos tengan una separación temporal de al menos 2.5 años en el caso de datos entre 1990-2010. En el caso de 1990_2025 se suele usar 10 años en su lugar. Permite escoger si se quiere usar el método de Theil Slopes o polifyt. También hay una descripción de características importantes a tener en cuenta sobre cada método.
    
Guarda un fichero del mismo tipo que el grid, pero con la variable tendencia añadida y la presión como tercera dimensión en /Data/tendency_levels/. El código con el que se guarda indica las fechas utilizadas, las profundidades y la resolución espacial usada.

**MapasTendenciasNiveles.ipynb** lee los datos de /Data/tendency_levels/ y calcula la media y desviación de la tendencia por cuencas, de forma que se representan estas variables en un mapa. Este mapa se guarda en data/plots/Mapas_Tendencias_Niveles/ indicando los datos necesarios para entender sus características. Permite decidir si representar la media calculada con Theil Slopes o polyfit, además de si se usa la media usual o la mediana para la media por cuencas.

### Deep Argo

**CalculaTendenciaNivelesArgo.ipynb** es para la comparación con los datos Argo. Basicamente este código es una adpatación de CalculaTendenciaNiveles.ipynb pero adaptada para poder comparar con los datos obtenidos de campañas Argo.


## Heat Flux

**HeatFluxVariables.ipynb**   añade las variables de densidad, capacidad calorífica a presión constante, superficie por pixel y máscara de forma que el fichero contiene todas las variables necesarias para el cálculo de flujos de calor. Lee de /Data/grid/, /Data/tendency_levels/ y del fichero total_filt.nc y devuelve el dataset en un archivo NetCDF en ./Data/Heat_vars/. Como siempre, el nombre del fichero indica las características del mismo.

**MapasHeatFlux.ipynb** lee de ./Data/Heat_vars/ y calcula la media y la desviación por cuencas, representando las mismas en un mapa en ./plots/Mapas_Heat_Flux/. También guarda un archivo con el flujo de calor medio y la desviación por cuencas en ./Data/Heat_flux/. Como siempre, el nombre del fichero indica las características del mismo.
    
### Global

**TotalHeatFlux.ipynb** calcula el flujo de calor global leyendo los datos de /Data/Heat_flux/. Devuelve un fichero csv que contiene información sobre el flujo de calor global, así como por cuencas y hemisferios e indicando los métodos resoluciones y fechas usadas.



---Ingles---
# New data

The file `DatosNuevos2026.txt` lists the files downloaded and added in March 2026.

**NewDataComparison.ipynb** contains two simple cells that print the filename, expocode, start date, and end date of matching files from `Data/direct_downloads/` and `Data/direct_downloads_nuevos/`. This makes it possible to verify whether files labeled as new actually belong to a new cruise.

# Identify QC values for later filtering

**QualityControlExtractor.ipynb** reads the data in `Data/direct_downloads/` and generates, for each section, a list of variables that include quality control information together with the QC values they contain. Knowing the QC flags used for each variable makes it possible to choose a more appropriate filtering strategy. It is recommended to consult the documentation:

[WOCE CTD Quality Codes](https://exchange-format.readthedocs.io/en/latest/quality.html)

# Read data and generate the metadata table

The `./Data/direct_downloads/` directory contains the original downloads organized by WOCE section. When a cruise includes a `section_id` and spans two or more WOCE sections, the corresponding files are duplicated into each section folder. If a cruise has no `section_id`, it is copied only into the folder corresponding to the section it most closely matches.

**ReadOriginalData.py** contains the `correct_sections()` function, which "corrects" the section assignments. The function uses the `section_id` variable (when available) from the NetCDF files to classify the data by section. Latitude and longitude values outside the target sections are removed, leaving only the data belonging to the desired section.

For the variables, it applies a quality-control filter that prioritizes QC flag **2** (good quality), and if unavailable, QC flag **1** (uncalibrated) or **0** (no QC assigned), ensuring that only valid measurements are retained. Among all possible salinity variable names, it automatically selects the correct one and filters salinity values to the physically meaningful range of 30–40 (in their respective units). If the variable `ctd_temperature-68` exists, it is converted to degrees Celsius by dividing by **1.00024**.

The script also extracts the sampling year from each file and uses it to rename the section files stored in `./Data/corrected_sections/`. In addition, it creates a `data.csv` file containing the filename, section, year, and reference for every cruise.

In the **27/03/2026** version, two dictionaries were added: one containing files with known issues together with explanatory comments, and another listing the different names that may refer to the same WOCE section.

Whenever new data are downloaded, it is important to inspect their `section_id` values using `SectionExtractor.ipynb`. If any new file contains a special case, the corresponding dictionary at the beginning of `ReadOriginalData.py` should be updated accordingly.

# Section maps and occupations

**PlotAllSectionsTracks.ipynb** reads the files in `./Data/corrected_sections/` and plots the track of each individual cruise on a map, labeling it with both the section name and filename. The figures are saved in `./Data/corrected_sections_plots/'SECTION'`. This provides an overview of the spatial coverage of each file.

**PlotOcean.ipynb** reads the files in `./Data/corrected_sections/` and plots all cruise tracks together on a single map, making it possible to visualize the overall spatial coverage of the dataset. The resulting figure is saved as `./Data/oceanSections.png`.

**PlotOccupations.ipynb** generates an **occupation diagram** from `./Data/data.csv`, extracting the sampling year and section to produce a scatter plot of occupations through time. The figure is saved in `./Data/` as `oceanOccupations.png`.

# TS diagrams

**plotTS.py** reads the data in `Data/corrected_sections/` and generates a Temperature–Salinity (TS) diagram for each file, saving the output in `./plots/'SECTION'`, where *SECTION* is the corresponding WOCE section.

The script includes a `raw` parameter. When `raw=False`, the diagram is plotted using automatically adjusted axes. When `raw=True`, no automatic scaling is applied, making anomalies easier to identify. This option is also linked to the point size used in the plot.

The figures are saved as:

- `raw_TS_INPUT_FILENAME` when `raw=True`

- `TS_INPUT_FILENAME` when `raw=False`

The script also allows the user to specify which sections should be plotted, avoiding unnecessary processing of all sections. A notebook version is also available.

# Apply the Hanning filter

**AplicaFiltroHanning.ipynb** reads the processed data from `Data/corrected_sections/` (previously generated by `ReadOriginalData.py`) and applies a Hanning filter to the variables of interest.

The notebook removes unnecessary variables and coordinates, keeping only those required for subsequent analyses, and saves the filtered files in `Data/corrected_sections_filtrado/` under their corresponding section folders.

A preliminary test can be performed using section **A01**, and the spatial resolution used during filtering can be adjusted.

The procedure first constructs the Hanning filter kernel and then convolves it with the selected variable, smoothing the vertical profiles. By default, a kernel width of **40 dbar** and a vertical resolution of **1 m** are used.

# Merge cruises

**UneCruises.ipynb** merges all processed cruises into a single dataset. It reads the filtered data from `Data/corrected_sections_filtrado/` and writes a NetCDF file to `Data/join/` containing all profiles from every cruise.

The dataset includes filtered temperature, salinity, and oxygen, together with derived density and specific heat capacity at constant pressure. The coordinates are latitude, longitude, sampling date, and source filename. The dimensions are `N_PROF × N_LEVELS`, where `N_PROF` is the total number of profiles and `N_LEVELS` spans the interpolated pressure levels.

# Create the basin mask

The `CreaCuencas` folder contains several MATLAB scripts that generate CSV files assigning a basin mask value to each map pixel.

The basin division follows Sarah G. Purkey's study:

> *Warming of Global Abyssal and Deep Southern Ocean Waters between the 1990s and 2000s: Contributions to Global Heat Content and Sea Level Rise Budgets.*

**CreateMask.ipynb** generates this basin mask and stores it as `Data/Mascara/mascara.nc`, containing the basin identifier and basin name associated with every pixel.

# Compute the occupation grid

**GridOccupation.ipynb** reads `Data/join/total_filt.nc` and creates `occupation.nc` in `Data/grid/`.

The notebook builds a latitude–longitude grid with user-defined resolution. For each grid cell, it stores the number of occupations and identifies which profiles from `total_filt.nc` fall within that cell.

The resulting dimensions are

$$

\text{latitude} \times \text{longitude} \times n_{\mathrm{prof}}

$$

where $n_{\mathrm{prof}}$ is the maximum number of occupations found in any grid cell.

The notebook also adds the variables `mask` and `basin` (basin name), using the mask generated by `CreaCuencas/CreateMask.ipynb`, so that basin information is directly included in the output file.

Finally, it computes bathymetry and the area of each grid cell (m²).

The notebook also plots the spatial distribution of occupations using a color map. These figures are saved in `/plots/Occupation_grids/`, with filenames indicating the grid resolution.

*Previous implementations of this step are contained in `grid_2025.ipynb` and `grid_2025.grid`. These versions also computed mean temperature and salinity for each profile, although that approach was later discarded.*

**Note:** `Locate.py` is used by these scripts.

# Trends and maps

**CalculaTendencias.ipynb** reads the selected-resolution grid from `/Data/grid/` together with temperature and salinity from `/Data/join/total_filt.nc`. It computes trends only for grid cells containing sufficient data.

By default, a valid grid cell must contain at least three temperature observations spanning at least **2.5 years**, although this threshold can be modified (for example, **10 years** is commonly used for the 1990–2025 period).

The notebook saves an updated grid containing the trend variable in `/Data/tendency/`, with filenames indicating the selected years, depth levels, and spatial resolution. It also generates maps in `/plots/Tendency_grids/` to visualize the spatial distribution of valid trends.

After extensive testing, an option was added to compute trends using either:

- the standard least-squares (`polyfit`) regression, or

- the **Theil–Sen estimator**.

Theil–Sen computes the median slope among all pairs of observations, making it more robust to outliers than ordinary least squares.

The notebook also includes a few lines of code to visualize the distribution of trend values by basin, allowing a qualitative assessment of whether trends cluster around characteristic values or exhibit large variability.

**MapasTendencias.ipynb** reads the files in `/Data/tendency/` and computes the mean and standard deviation of trends for each basin. These statistics are displayed on maps saved in `plots/Mapas_Tendencias/`.

The notebook allows the user to choose between Theil–Sen and ordinary least-squares trends, and between the arithmetic mean and the median when averaging trends within each basin.

## Trends by depth level

**CalculaTendenciaNiveles.ipynb** computes trends independently at each pressure level using the data in `/Data/grid/` and `/Data/join/total_filt.nc`.

The default criteria require at least three observations separated by at least **2.5 years** for the 1990–2010 period, while **10 years** is typically used for analyses covering 1990–2025.

The notebook allows the user to choose either the Theil–Sen estimator or ordinary least squares (`polyfit`) and includes a discussion of the strengths and limitations of each method.

The resulting files are stored in `/Data/tendency_levels/`, with pressure as the third dimension. Filenames indicate the selected years, pressure range, and spatial resolution.

**MapasTendenciasNiveles.ipynb** reads these files and computes basin-scale mean trends and standard deviations, displaying them on maps stored in `plots/Mapas_Tendencias_Niveles/`. As before, users can choose between Theil–Sen or least-squares trends and between mean or median basin statistics.

## Deep Argo

**CalculaTendenciaNivelesArgo.ipynb** is designed for comparison with Deep Argo observations. It is essentially an adaptation of `CalculaTendenciaNiveles.ipynb` that has been modified to process Deep Argo datasets.

# Heat flux

**HeatFluxVariables.ipynb** adds density, specific heat capacity at constant pressure, grid-cell area, and basin mask to produce a dataset containing all variables required for heat flux calculations.

It reads data from `/Data/grid/`, `/Data/tendency_levels/`, and `total_filt.nc`, and writes a NetCDF dataset to `./Data/Heat_vars/`. As throughout the workflow, filenames encode the processing parameters used.

**MapasHeatFlux.ipynb** reads the datasets in `./Data/Heat_vars/`, computes basin-averaged heat fluxes and their standard deviations, and plots the results in `./plots/Mapas_Heat_Flux/`.

It also saves a dataset containing the mean basin heat fluxes and their standard deviations in `./Data/Heat_flux/`. Again, filenames encode the processing settings.

## Global heat flux

**TotalHeatFlux.ipynb** computes the global heat flux from the datasets stored in `/Data/Heat_flux/`.

The notebook generates a CSV file summarizing the global heat flux, as well as basin-scale and hemispheric heat fluxes, together with the methods, spatial resolutions, and time periods used in the calculations.