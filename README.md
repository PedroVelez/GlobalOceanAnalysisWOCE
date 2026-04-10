
- Identificar sección de los datos crudos:
    - La función GetSectionFiles.py , analiza la carpeta .Data/direct_downloads cuando está estaba sin clasificar los archivos por secciones. Devuelve el listado de ficheros y secciones asociadas, cuando las hay, pues en algunas ocasiones no existe 'section_id'
    - SectionExtractor.py, que lee de .Data/direct_downloads  da una lista de las variables section_id de cada archivo, lo que permite identificar problemas. De esta forma se tiene en cuenta todos los posibles errores que puedan llevar a perdidas de datos por el camino.

- Datos nuevos:
    - En el fichero DatosNuevos2026.txt, se encontrarán los archivos descargados que fueron añadidos en marzo de 2026.
    - El notebook NewDataComparison.ipynb, se encuentran dos pequeñas celdas que imprimen el nombre del archivo, el expocode, la fecha de inicio y la de final de la carpeta Data/direct_downloads/ y Data/direct_downloadas_nuevos/ de una misma sección, de forma que se puede comprobar si los ficheros etiquetados como nuevos realmente pertenecen a una campaña nueva.

- Identificar valores qc para posterior filtrado: QualityControlExtractor.ipynb
    Esta función usa los datos de Data/direct_downloads/ y crea una lista por secciones de las variables que tienen control de calidad y que valores tienen estos. Sabiendo los distintos valores de control de calidad que tienen las variables en los archivos, se puede escoger un filtrado más apropiado. Se recomienda revisar la documentación: [WOCE CTD Quality Codes](https://exchange-format.readthedocs.io/en/latest/quality.html)
    

- Leer datos y tabla: ReadOriginalData.py
    En ./Data/direct_downloads/, están las las descargas crudas de internet ya organizadas por secciones WOCE. Cuando una campaña tenia 'section_id' y se realizaba de manera conjunta en dos o más secciones WOCE we copiaba por duplicado en las carpetas de las secciones.  Cuando un campaña no tiene 'section_id' se copia solamente en una carpeta, la que más se asemeja a la sección correspondiente.
    En ReadOriginalData.py está la función correct_sections() que 'corrige' las secciones. Está función emplea la variable 'section_id' (cuando existe) de los archivos netcdf para su clasificación por secciones. Los valores de latitud y longitud que no pertenezcan a secciones de interés son recortados, dejando únicamente los datos de secciones puras. Con respecto a las variables aplica un filtro de control de calidad con etiqueta 2 (Buenas calidad) para usar solo medidas eficientes. Además, de entre todos los posibles nombres de salinidad, se queda con el que corresponde y recorta para que los datos de salinidad estén solo entre 30 y 40 en sus respectivas unidades. Si existe la variable 'ctd_temperature-68' la convierte a grados celsius dividiendo entre 1.00024.
    
    También extrae los años de muestreo del archivo y los usas para modificar los nombres de los ficheros de secciones en la carpeta de secciones corregidas. También crea un fichero data.csv con nombres de los ficheros, su sección, año y referencia.  En la versión del 27/03/2026, se añade un diccionario con ficheros que tienen algún problema y su respectivo comentario de información, y otro diccionario que indica que distintos nombres puede tener una misma sección. 

    Es importante tener en cuenta que si se descargan nuevos datos hay que revisar sus section_id con Section_Extrator.ipynb, para ver si alguno de los nuevos archivos presenta una peculiaridad y en su caso, añadir esta peculiaridad al correspondiente diccionario que se encuentra al principio del archivo ReadOriginalData.py.

- Mapa de secciones:
    - PlotAllSections.py, lee de Data/corrected_sections/  y representa la sección que recorre cada archivo en el mapa una por una con el nombre de su sección y el del archivo, guardándolo en ./plots/'SECTION'.
    - El archivo PlotOcean.py, lee de Data/corrected_sections/ y representa la sección que recorre cada archivo en el mapa, todas en un mismo mapa, de forma que se puede ver las zonas de las que se tienen dados. Guarda el mapa pintado en ./plots/, bajo el nombre "oceans_sections.png"

- Gráfica de ocupaciones: PlotSectionYears.py
    Dibuja la gráfica de ocupaciones a partir de Data/data.csv, extrayendo el año y la sección de forma que se generá una gráfica de puntos. La gráfica obtenida se guarda en ./plots/ bajo el nombre occupations.png


- Diagramas TS: plotTS.py
    Está función lee los datos de Data/corrected_sections/ y hace un diagrama TS para cada archivo, guardándolo en ./plots/'SECTION' donde section es la sección que le corresponde. Contiene el parámetro raw, que si se le da el valor 'FALSE' representa de forma ordinaria, y si se le da el valor 'TRUE' representa en crudo de forma que es más sencillo identificar anomálias, es un parámetro más ligado al tamaño de los puntos. Estos diagramas se guardan con nombre "raw_TS_NOMBRE_DEL_FICHERO_EN_LA_CARPETA_DE_ENTRADA" si raw = 'TRUE' o igual pero sin el raw en caso de raw = 'FALSE'. También da la opción de indicar que secciones representar, por lo que en caso de solo necesitar representar una única sección, no hay que repetir las demás.

- Versión filtrada: aplicaFiltroHanning.ipynb
    Este jupyternotebook lee los datos de Data/corrected_sections/, que ya han sido procesados con ReadOriginalData.py y le aplica un filtro Hanning a las variables de interes. Limpia el archivo para que solo tenga las variables y coordenadas necesarias, ya con el filtro aplicado. Devuelve estos ficheros corregidos en la carpeta Data/corrected_sections_filtrado/ en su correspondiente sección. En el notebook se puede ejecutar una prueba previa con la sección A01, además permite escoger la resolución de los puntos del filtrado. 

    El procedimiento consiste en crear la curva del filtro hanning para luego hacer una convolución con la variable de interes de forma que está se ajusta a la curva y suaviza los perfiles. Por defecto se usa un filtro con 40 dbar como ancho de kernel y una resolución espacial de 1 m.

- Unir todas los datos en una matriz: uneCruises.ipynb.
    Este jupyternotebook lee los datos de Data/corrected_sections_filtrado/, a los que ya se les ha aplicado el filtro Hanning. Guarda en Data/join/ un fichero .nc que contiene todos los datos de todos los archivos. Las variables de este fichero son Temperatura, salinidad, y oxígeno filtrados. Como coordenas tiene latitud, longitud, fecha y nombre del fichero de origen. Por último como dimensiones tiene N_PROFxN_LEVELS donde N_PROF es la suma de todos los perfiles que habían en los ficheros y N_LEVES va desde 0 hasta el máximo de presión interpolada.
    
- Calcula Matriz de ocupaciones: grid.ipynb y grid.py 
    - El archivo grid.ipynb lee los datos de Data/join/total_filt.nc y devuelve un archivo con el nombre grid_1_9019.nc en la carpeta Data/grid/. Recorta los datos para que las presiones esten entre 1990 y 2010, aunque esto se puede cambiar. Luego crea un grid de latitud, longitud y profundidad con paso 1 y profundidad con resolución 100 dbar. Crea un dataset en el que las dimensiones son latitud, longitud, profundidad y tiempo, y las variables las temperaturas, salinidades y oxigenos medios. De está forma para cada grid, cada profundidad y cada fecha hay un valor de temperatura, salinidad y oxigeno.
    - El archivo grid.py contiene una función que es usada en el código anterior. En concreto occupation_matrix, que devuelve los arrays de temperatura, salinidad y oxigeno con las dimensiones antes mencionadas. Su finalidad es auxiliar, por si solo no hace nada.

    
- Tendencias y mapas: CalculaTendencias y MapasTendencias.ipynb

