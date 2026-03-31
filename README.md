
- Identificar sección de los datos crudos:
    - La función GetSectionFiles.py , analiza la carpeta .Data/direct_downloads cuando está estaba sin clasificar los archivos por secciones. Devuelve el listado de ficheros y secciones asociadas, cuando las hay, pues en algunas ocasiones no existe 'section_id'
    - SectionExtractor.py, que lee de .Data/direct_downloads  da una lista de las variables section_id de cada archivo, lo que permite identificar problemas. De esta forma se tiene en cuenta todos los posibles errores que puedan llevar a perdidas de datos por el camino.

- Datos nuevos:
    En el fichero DatosNuevos2026.txt, se encontrarán los archivos descargados que fueron añadidos en marzo de 2026.
    - El notebook NewDataComparison.ipynb, se encuentran dos pequeñas celdas que imprimen el nombre del archivo, el expocode, la fecha de inicio y la de final de la carpeta Data/direct_downloads/ y Data/direct_downloadas_nuevos/ de una misma sección, de forma que se puede comprobar si los ficheros etiquetados como nuevos realmente pertenecen a una campaña nueva.

- Leer datos y tabla: ReadOriginalData.py
    En ./Data/direct_downloads/, están las las descargas crudas de internet ya organizadas por secciones WOCE. Cuando una campaña tenia 'section_id' y se realizaba de manera conjunta en dos o más secciones WOCE we copiaba por duplicado en las carpetas de las secciones.  Cuando un campaña no tiene 'section_id' se copia solamente en una carpeta, la que más se asemeja a la sección correspondiente.
    En ReadOriginalData.py está la función correct_sections() que 'corrige' las secciones. Está función emplea la variable 'section_id' (cuando existe) de los archivos netcdf para su clasificación por secciones. Los valores de latitud y longitud que no pertenezcan a secciones de interés son recortados, dejando únicamente los datos de secciones puras. Con respecto a las variables aplica un filtro de control de calidad con etiqueta 2 (Buenas calidad) para usar solo medidas eficientes. Además, de entre todos los posibles nombres de salinidad, se queda con el que corresponde y recorta para que los datos de salinidad estén solo entre 30 y 40 en sus respectivas unidades. Si existe la variable 'ctd_temperature-68' la convierte a grados celsius dividiendo entre 1.00024.
    
    También extrae los años de muestreo del archivo y los usas para modificar los nombres de los ficheros de secciones en la carpeta de secciones corregidas. También crea un fichero data.csv con nombres de los ficheros, su sección, año y referencia.  En la versión del 27/03/2026, se añade un diccionario con ficheros que tienen algún problema y su respectivo comentario de información, y otro diccionario que indica que distintos nombres puede tener una misma sección. 

- Mapa de secciones:
    - PlotAllSections.py, lee de Data/corrected_sections/  y representa la sección que recorre cada archivo en el mapa una por una con el nombre de su sección y el del archivo, guardándolo en ./plots/'SECTION'.
    - El archivo PlotOcean.py, lee de Data/corrected_sections/ y representa la sección que recorre cada archivo en el mapa, todas en un mismo mapa, de forma que se puede ver las zonas de las que se tienen dados. Guarda el mapa pintado en ./plots/, bajo el nombre "oceans_sections.png"

- Gráfica de ocupaciones: PlotSectionYears.py
    Dibuja la gráfica de ocupaciones a partir de Data/data.csv, extrayendo el año y la sección de forma que se generá una gráfica de puntos. La gráfica obtenida se guarda en ./plots/ bajo el nombre occupations.png


- Diagramas TS: plotTS.py
    Está función lee los datos de Data/corrected_sections/ y hace un diagrama TS para cada archivo, guardándolo en ./plots/'SECTION' donde section es la sección que le corresponde. Contiene el parámetro raw, que si se le da el valor 'FALSE' representa de forma ordinaria, y si se le da el valor 'TRUE' representa en crudo de forma que es más sencillo identificar anomálias, es un parámetro más ligado al tamaño de los puntos. Estos diagramas se guardan con nombre "raw_TS_NOMBRE_DEL_FICHERO_EN_LA_CARPETA_DE_ENTRADA" si raw = 'TRUE' o igual pero sin el raw en caso de raw = 'FALSE'. También da la opción de indicar que secciones representar, por lo que en caso de solo necesitar representar una única sección, no hay que repetir las demás.

- Versión filtrada: aplicaFiltroHanning.ipynb
- Unir todas los datos en una matriz -  uneCruises.ipynb.
- Calcula Matriz de ocupaciones: grid.ipynb y grid.py (en scripts_samuel)
- Tendencias y mapas: CalculaTendencias y MapasTendencias.ipynb

