
- Identificar sección de los datos crudos:
    - La función GetSectionFiles.py , analiza la carpeta .Data/direct_downloads cuando está estaba sin clasificar los archivos por secciones. Devuelve el listado de ficheros y secciones asociadas, cuando las hay, pues en algunas ocasiones no existe 'section_id'
    - SectionExtractor.py, que lee de .Data/direct_downloads  da una lista de las variables section_id de cada archivo, lo que permite identificar problemas. De esta forma se tiene en cuenta todos los posibles errores que puedan llevar a perdidas de datos por el camino.

- Datos nuevos:
    - En el fichero DatosNuevos2026.txt, se encontrarán los archivos descargados que fueron añadidos en marzo de 2026.
    - El notebook NewDataComparison.ipynb, se encuentran dos pequeñas celdas que imprimen el nombre del archivo, el expocode, la fecha de inicio y la de final de la carpeta Data/direct_downloads/ y Data/direct_downloadas_nuevos/ de una misma sección, de forma que se puede comprobar si los ficheros etiquetados como nuevos realmente pertenecen a una campaña nueva.

- Identificar valores qc para posterior filtrado: QualityControlExtractor.ipynb

    Esta función usa los datos de Data/direct_downloads/ y crea una lista por secciones de las variables que tienen control de calidad y que valores tienen estos. Sabiendo los distintos valores de control de calidad que tienen las variables en los archivos, se puede escoger un filtrado más apropiado. Se recomienda revisar la documentación: [WOCE CTD Quality Codes](https://exchange-format.readthedocs.io/en/latest/quality.html)
    

- Leer datos y tabla: ReadOriginalData.py

    En ./Data/direct_downloads/, están las las descargas crudas de internet ya organizadas por secciones WOCE. Cuando una campaña tenia 'section_id' y se realizaba de manera conjunta en dos o más secciones WOCE se copiaba por duplicado en las carpetas de las secciones.  Cuando un campaña no tiene 'section_id' se copia solamente en una carpeta, la que más se asemeja a la sección correspondiente.

    En ReadOriginalData.py está la función correct_sections() que 'corrige' las secciones. Está función emplea la variable 'section_id' (cuando existe) de los archivos netcdf para su clasificación por secciones. Los valores de latitud y longitud que no pertenezcan a secciones de interés son recortados, dejando únicamente los datos de secciones puras. Con respecto a las variables aplica un filtro de control de calidad con etiqueta 2 (Buenas calidad) y en su defecto 1 (Sin calibrar) o 0 (no asociado) para usar solo medidas eficientes. Además, de entre todos los posibles nombres de salinidad, se queda con el que corresponde y recorta para que los datos de salinidad estén solo entre 30 y 40 en sus respectivas unidades. Si existe la variable 'ctd_temperature-68' la convierte a grados celsius dividiendo entre 1.00024.
    
    También extrae los años de muestreo del archivo y los usa para modificar los nombres de los ficheros de secciones en la carpeta ./Data/corrected_sections/. También crea un fichero data.csv con nombres de los ficheros, su sección, año y referencia.  En la versión del 27/03/2026, se añade un diccionario con ficheros que tienen algún problema y su respectivo comentario de información, y otro diccionario que indica que distintos nombres puede tener una misma sección. 

    Es importante tener en cuenta que si se descargan nuevos datos hay que revisar sus section_id con Section_Extrator.ipynb, para ver si alguno de los nuevos archivos presenta una peculiaridad y en su caso, añadir esta peculiaridad al correspondiente diccionario que se encuentra al principio del archivo ReadOriginalData.py.

- Mapa de secciones:
    - PlotAllSections.py, lee de Data/corrected_sections/  y representa la sección que recorre cada archivo en el mapa una por una con el nombre de su sección y el del archivo, guardándolo en ./plots/'SECTION'. Esta es útil para saber que datos están almacenados de cada archivo.
    - El archivo PlotOcean.py, lee de Data/corrected_sections/ y representa la sección que recorre cada archivo en el mapa, todas en un mismo mapa, de forma que se puede ver las zonas de las que se tienen dados. Guarda el mapa pintado en ./plots/, bajo el nombre "oceans_sections.png"

- Gráfica de ocupaciones: PlotSectionYears.py

    Dibuja la gráfica de ocupaciones a partir de Data/data.csv, extrayendo el año y la sección de forma que se generá una gráfica de puntos. La gráfica obtenida se guarda en ./plots/ bajo el nombre occupations.png


- Diagramas TS: plotTS.py

    Está función lee los datos de Data/corrected_sections/ y hace un diagrama TS para cada archivo, guardándolo en ./plots/'SECTION' donde section es la sección que le corresponde. Contiene el parámetro raw, que si se le da el valor 'FALSE' representa de forma ordinaria, y si se le da el valor 'TRUE' representa en crudo de forma que es más sencillo identificar anomálias, es un parámetro más ligado al tamaño de los puntos. Estos diagramas se guardan con nombre "raw_TS_NOMBRE_DEL_FICHERO_EN_LA_CARPETA_DE_ENTRADA" si raw = 'TRUE' o igual pero sin el raw en caso de raw = 'FALSE'. También da la opción de indicar que secciones representar, por lo que en caso de solo necesitar representar una única sección, no hay que repetir las demás.

- Versión filtrada: aplicaFiltroHanning.ipynb

    Este jupyternotebook lee los datos de Data/corrected_sections/, que ya han sido procesados con ReadOriginalData.py y le aplica un filtro Hanning a las variables de interes. Limpia el archivo para que solo tenga las variables y coordenadas necesarias, ya con el filtro aplicado. Devuelve estos ficheros corregidos en la carpeta Data/corrected_sections_filtrado/ en su correspondiente sección. En el notebook se puede ejecutar una prueba previa con la sección A01, además permite escoger la resolución de los puntos del filtrado. 

    El procedimiento consiste en crear la curva del filtro hanning para luego hacer una convolución con la variable de interes de forma que está se ajusta a la curva y suaviza los perfiles. Por defecto se usa un filtro con 40 dbar como ancho de kernel y una resolución espacial de 1 m.

- Unir todas los datos en una matriz: uneCruises.ipynb.

    Este jupyternotebook lee los datos de Data/corrected_sections_filtrado/, a los que ya se les ha aplicado el filtro Hanning. Guarda en Data/join/ un fichero .nc que contiene todos los datos de todos los archivos. Las variables de este fichero son Temperatura, salinidad, y oxígeno filtrados, además de las densidades y capacidades calorificas a presión constante calculadas. Como coordenas tiene latitud, longitud, fecha y nombre del fichero de origen. Por último como dimensiones tiene N_PROFxN_LEVELS donde N_PROF es la suma de todos los perfiles que habían en los ficheros y N_LEVES va desde 0 hasta el máximo de presión interpolada.
    

- Crear división por cuencas: CreateMask.ipynb
    - En la carpeta CreaCuencas hay varios códigos en matlab que crean archivos csv, indicando el valor de la máscara para cada pixel del mapa. La división por cuencas usada se extrae de el artículo de Sarah G.Purkey: [Warming of Global Abyssal and Deep Southern Ocean Waters between the 1990s and 2000s: Contributions to Global Heat Content and Sea Level Rise Budgets](https://journals.ametsoc.org/view/journals/clim/23/23/2010jcli3682.1.xml?tab_body=pdf)

    - En el fichero CreateMask.ipynb se crea dicha máscara devolviendo un archivo netcdf en Data/Mascara/mascara.nc, que contiene el valor de cuenca asociado a cada pixel y el nombre


- Calcula Matriz de ocupaciones: grid.ipynb
    - El archivo grid.ipynb lee los datos de Data/join/total_filt.nc y devuelve un archivo con el nombre occupation.nc en la carpeta Data/grid/. La idea es crear un grid de latitudes y longitudes de resolución ajustable, de forma que para cada pixel del mapa se pueda ver el número de ocupaciones para ese punto, y además que perfiles del archivo total_filt.nc son los que contiene. De esta forma las dimensiones son de $latitud \times longitud \times n_{prof}$, donde $n_{prof}$ es el número máximo de ocupaciones que se esperan para cualquier pixel, es decir, cada punto tendrá un n inferior a $n_{prof}$. También tiene unas celdas que añaden una las variables mask y basin (nombre de cuenca) que corresponden a la máscara creada en CreaCuencas/CreateMask.ipynb, de forma que la máscara está ya guardada en los ficheros con el nombre de cada cuenca. Por último, también proporciona los datos de batimetría y la superficie de cada pixel en $m^2$

    Este mismo notebook también representa las ocupaciones por cada punto del grid en un mapa y una barra de color, de forma que se puede ver el número de perfiles por punto. Las figuras que se obtienen se guardan en /plots/Occupation_grids/ con un nombre de archivo distinto según la resolución usada.  
    - Las versiones anteriores de está parte se encuentran contenidas en los archivos: grid_2025.ipynb y grid_2025.grid. Estas incluyen un cálculo descartado de temperatura y salinidad medias de cada perfil.
        - Nota: La función locate.py es usada en estos script
    


- Tendencias y mapas: CalculaTendencias.ipynb y MapasTendencias.ipynb
    - El fichero CalculaTendencias.ipynb extrae el grid de la resolución deseada de /Data/grid/ y los datos de temperatura y salinidad de /Data/join/total_filt.nc. Con estos archivos calcula la tendencia en los pixeles donde hayan valores suficientes como para calcular la misma. En principio el criterio es que dicho pixel contenga al menos 3 datos de temperatura y que estos tengan una separación temporal de al menos 2.5 años, aunque esto último puede variar si se desea, por ejemplo para 1990-2025 se suele usar 10 años en su lugar. Guarda un fichero del mismo tipo que el grid, pero con la variable tendencia añadida en /Data/tendency/, indicando años en los que se ha filtrado, niveles y resolución. También guarda mapas en /plots/Tendency_grids/ que permiten ver las tendencias en los puntos en los que existen permitiendo ver si los resultados son buenos.

    Tras varias pruebas, se decidio añadir una variable que indica si se quiere usar el método de ajuste de Theil Slopes o el ajuste por mínimos cuadrados usual de polyfit. Theil Slopes toma la mediana de las pendientes de todos los pares de puntos, por lo que en algunos casos será más robusta estadísticamente, ya que da la sensación de que ignora datos atípicos. 
    
    Por último, hay unas breves líneas de código que sirven para la representación de puntos de la distribución de puntos de tendencia por cuencas, de forma que se puede ver si estas se agrupan sobre un valor, o por el contrario las desviaciones dan lugar a poca significancia estadística.

    - El fichero MapasTendencias.ipynb lee los datos de /Data/tendency/ y calcula la media y desviación de la tendencia por cuencas, de forma que se representan estas variables en un mapa. Este mapa se guarda en plots/Mapas_Tendencias/ indicando los datos necesarios para entender sus características. Permite decidir si representar la media calculada con Theil Slopes o polyfit, además de si se usa la media usual o la mediana para la media por cuencas

- Tendencias por niveles: CalculaTendenciaNiveles.ipynb y MapasTendenciasNiveles.ipynb

    - Este fichero lee los datos de /Data/grid/ y /Data/join/total_filt.nc y calcula la tendencia en los pixeles donde hayan valores suficientes como para calcular la misma. En principio el criterio es que dicho pixel contenga al menos 3 datos de temperatura y que estos tengan una separación temporal de al menos 2.5 años en el caso de datos entre 1990-2010. En el caso de 1990_2025 se suele usar 10 años en su lugar. Permite escoger si se quiere usar el método de Theil Slopes o polifyt. También hay una descripción de características importantes a tener en cuenta sobre cada método.
    
    Guarda un fichero del mismo tipo que el grid, pero con la variable tendencia añadida y la presión como tercera dimensión en /Data/tendency_levels/. El código con el que se guarda indica las fechas utilizadas, las profundidades y la resolución espacial usada.

    - El fichero MapasTendenciasNiveles.ipynb lee los datos de /Data/tendency_levels/ y calcula la media y desviación de la tendencia por cuencas, de forma que se representan estas variables en un mapa. Este mapa se guarda en plots/Mapas_Tendencias_Niveles/ indicando los datos necesarios para entender sus características. Permite decidir si representar la media calculada con Theil Slopes o polyfit, además de si se usa la media usual o la mediana para la media por cuencas.

- Creación de ficheros para el calculo de flujos de calor: HeatFluxVariables.ipynb
    Este script añade las variables de densidad, capacidad calorífica a presión constante, superficie por pixel y máscara de forma que el fichero contiene todas las variables necesarias para el cálculo de flujos de calor. Lee de /Data/grid/, /Data/tendency_levels/ y del fichero total_filt.nc y devuelve el dataset en un archivo NetCDF en ./Data/Heat_vars/. Como siempre, el nombre del fichero indica las características del mismo.

- Mapas de flujos de calor: MapasHeatFlux.ipynb
    El script lee de ./Data/Heat_vars/ y calcula la media y la desviación por cuencas, representando las mismas en un mapa en ./plots/Mapas_Heat_Flux/. También guarda un archivo con el flujo de calor medio y la desviación por cuencas en ./Data/Heat_flux/. Como siempre, el nombre del fichero indica las características del mismo.
    
- Flujo de Calor global: TotalHeatFlux.ipynb
    En este se calcula el flujo de calor global leyendo los datos de /Data/Heat_flux/. Devuelve un fichero csv que contiene información sobre el flujo de calor global, así como por cuencas e indicando los métodos resoluciones y fechas usadas.

- Tendencias para la comparación con los datos Argo: CalculaTendenciaNivelesArgo.ipynb
    Basicamente este código es una adpatación de CalculaTendenciaNiveles.ipynb pero adaptada para poder comparar con los datos obtenidos de campañas Argo.
    

