
- Identificar sección de los datos crudos:
    - La función get_Section_files.py , analiza la carpeta .Data/direct_downloads cuando está estaba sin clasificar los archivos por secciones. Devuelve el listado de ficheros y secciones asociadas, cuando las hay, pues en algunas ocasiones no existe 'section_id'
    - Section_extractor.py, que lee de .Data/direct_downloads  da una lista de las variables section_id de cada archivo, lo que permite identificar problemas. De esta forma se tiene en cuenta todos los posibles errores que puedan llevar a perdidas de datos por el camino.

- Datos nuevos:
    En el fichero DatosNuevos2026.txt, se encontrarán los archivos descargados que fueron añadidos en marzo de 2026

- Leer datos y tabla: ReadOriginalData.py
    En ./Data/direct_downloads/, están las las descargas crudas de internet ya organizadas por secciones WOCE. Cuando una campaña tenia 'section_id' y se realizaba de manera conjunta en dos o más secciones WOCE we copiaba por duplicado en las carpetas de las secciones.  Cuando un campaña no tiene 'section_id' se copia solamente en una carpeta, la que más se asemeja a la sección correspondiente.
    En ReadOriginalData.py está la función correct_sections() que 'corrige' las secciones. Está función emplea la variable 'section_id' (cuando existe) de los archivos netcdf para su clasificación por secciones. Los valores de latitud y longitud que no pertenezcan a secciones de interés son recortados, dejando únicamente los datos de secciones puras. Con respecto a las variables aplica un filtro de control de calidad con etiqueta 2 (Buenas calidad) para usar solo medidas eficientes. Además, de entre todos los posibles nombres de salinidad, se queda con el que corresponde y recorta para que los datos de salinidad estén solo entre 30 y 40 en sus respectivas unidades. Si existe la variable 'ctd_temperature-68' la convierte a grados celsius dividiendo entre 1.00024.
    
    También extrae los años de muestreo del archivo y los usas para modificar los nombres de los ficheros de secciones en la carpeta de secciones corregidas. También crea un fichero data.csv con nombres de los ficheros, su sección, año y referencia.  En la versión del 27/03/2026, se añade un diccionario con ficheros que tienen algún problema y su respectivo comentario de información, y otro diccionario que indica que distintos nombres puede tener una misma sección. 

- Mapa de secciones:
    plot_all_sections.py, lee de Data/corrected_sections/  y representa la sección que recorre cada archivo en el mapa una por una con el nombre de su sección y el del archivo, guardándolo en ./plots/'SECTION'.

- Diagramas TS y mapa: plotTS.py
- Versión filtrada: aplicaFiltroHanning.ipynb
- Unir todas los datos en una matriz -  uneCruises.ipynb.
- Calcula Matriz de ocupaciones: grid.ipynb y grid.py (en scripts_samuel)
- Tendencias y mapas: CalculaTendencias y MapasTendencias.ipynb

