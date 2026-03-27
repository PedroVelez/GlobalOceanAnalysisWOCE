
- Identificar sección de los datos crudos:
    La función get_Section_files.py , analiza la carpeta .Data/direct_downloads cuando está estaba sin clasificar los archivos por secciones. Te devuelve y clasifica los archivos en carpetas por secciones

- Datos nuevos:
    En el fichero Datos nuevos.txt, se encontrarán los archivos descargados que fueron añadidos en marzo de 2026

- Leer datos y tabla: ReadOriginalData.py
    ./Data/direct_downloads/, están las las descargas crudas de internet, para corregirlas tienes que usar la función correct_sections() en data.py. Está función emplea la variable 'section_id' de los archivos netcdf para su clasificación por secciones. Los valores de latitud y longitud que no pertenezcan a secciones de interés son recortados, dejando únicamente los datos de secciones puras. Con respecto a las variables aplica un filtro de control de calidad con etiqueta 2 (Buenas calidad) para usar solo medidas eficientes. De entre todos los posibles nombres de salinidad, se queda con el que corresponde y recorta para que los datos de salinidad esten solo entre 30 y 40 en sus respectivas unidades. Si existe la variable 'ctd_temperature-68' la convierte a grados celsius dividiendo entre 1.00024. Extrae los años de muestreo del archivo y los usas para los nombres de los ficheros de secciones corregidas. También crea un fichero .csv con nombres de los ficheros, su sección, año y referencia. En la versión del 27/03/2026, se añade un diccionario con ficheros que tienen algún problema y su respectivo comentario de información, y otro diccionario que indica que distintos nombres puede tener una misma sección. Previmente se recomienda ejecutar el Section_extractor.py, que da una lista de las variables section_id de cada archivo, lo que permite identificar problemas. De esta forma se tiene en cuenta todos los posibles errores que puedan llevar a perdidas de datos por el camino.

- Mapa de secciones:
    Dado el directorio con los datos corregidos y el directorio de guardado, representa la sección que recorre cada archivo en el mapa una por una con el nombre de su sección y el del archivo. La salida son un conjunto de gráficas que se guardan en la carpeta plots y en su respectiva carpeta de sección.

- Diagramas TS y mapa: plotTS.py
 - Versión filtrada: aplicaFiltroHanning.ipynb
- Unir todas los datos en una matriz -  uneCruises.ipynb.
- Calcula Matriz de ocupaciones: grid.ipynb y grid.py (en scripts_samuel)
- Tendencias y mapas: CalculaTendencias y MapasTendencias.ipynb

