close all
clear all

iregion=1;

switch iregion
    case 1
        img = imread('./Mapas/NA.png');
        l=1;
    case 2
        img = imread('./Mapas/SA.png');
        l=2;
    case 3
        img = imread('./Mapas/SI.png');
        l=3;

    case 4
        img = imread('./Mapas/NI.png');
        l=4;
    case 5
        img = imread('./Mapas/SP.png');
        l=5;

    case 6
        img = imread('./Mapas/NP.png');
        l=6;

end

%%

Slongs=[-100 43;-75 20; 20 145;43 100;145 295;100 295];
Slats= [  0  90;-90  0;-90   0; 0  90;-90   0;  0  90];


% Creamos un eje que ocupe toda la ventana
ax_fondo = axes('Position', [0.1 0.1 0.8 0.8]);
image(img);
axis off;

%% Creamos un segundo eje exactamente en la misma posición
ax_mapa = axes('Position', [0.1 0.1 0.8 0.8], 'Color', 'none');
m_proj('mollweide', 'long', Slongs(l,:), 'lat', Slats(l,:));
m_coast('color', 'k', 'linewidth', 1);hold on
m_grid;

set(findobj(gca,'type','patch','tag','m_grid_color'),'facecolor','none');
set(findobj(gca,'type','patch','tag','m_grid_color'),'facecolor','none');
set(findobj(gca,'type','patch','tag','m_grid'),'facecolor','none');
set(gca, 'Color', 'none');


%[lon,lat] = m_ginput;
%writetable(table(lon, lat), 'NAWest.csv')