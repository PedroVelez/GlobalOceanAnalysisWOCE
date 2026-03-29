file='SAEast.csv';

D=readtable(strcat('./Cuencas/',file));
lat = D.lat;
lon = D.lon;
% lat y lon deben ser vectores columna
kmlwrite(strcat(file(1:end-4),'.kml'),lat, lon, 'Name',file(1:end-4));
