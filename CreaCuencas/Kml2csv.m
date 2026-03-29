file='SAEast';


puntos_editados = readgeotable(strcat(file,'.kml'));
% Las coordenadas suelen venir en una columna llamada 'Shape'
coordenadas = puntos_editados.Shape;
lat = coordenadas.Latitude;
lon = coordenadas.Longitude;
writetable(table(lon, lat),strcat(file,'.csv'))