D=readtable('./Cuencas/SPWest.csv');
lat = D.lat;
lon = D.lon;

% lat y lon deben ser vectores columna
kmlwrite('puntos_mapa.kml',lat, lon, 'Name', 'Mis Puntos');

puntos_editados = readgeotable('salida.kml');
% Las coordenadas suelen venir en una columna llamada 'Shape'
coordenadas = puntos_editados.Shape;
lat = coordenadas.Latitude;
lon = coordenadas.Longitude;