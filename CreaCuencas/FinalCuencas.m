close all
clear all

%% Atlatnico
figure
m_proj('robinson','lon',[-90 100]);
m_coast('patch',[.7 1 .7],'edgecolor','none'); hold on
m_grid

file='./Cuencas/NAEast.csv'
D=readtable(file);
m_line(D.lon,D.lat,'color','b','linewi',3)
m_hatch(D.lon,D.lat,'single',45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/NAWest.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/NACaribe.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/SAEast.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/SAWestNorth.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-30,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/SAEastNamibia.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/SAWestMalvinas.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/SouthAfrica.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/SACentralAntartica.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

%No sale
D=readtable(file);
file=('./Cuencas/SPEastAntartica.csv');
m_plot(D.lon-360,D.lat,'b','linewidth',3)
m_hatch(D.lon-360,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')
CreaFigura(gcf,strcat(mfilename,'01'),[7])

%% India
figure
m_proj('robinson','lon',[-80 180]);
m_coast('patch',[.7 1 .7],'edgecolor','none'); hold on
m_grid

file=('./Cuencas/EastMadagascar.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/SouthMadagascar.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/NIWest.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/NICentral.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/NICentralEast.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/NIEast.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/SouthAfrica.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/SACentralAntartica.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/SouthAustralia.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/SIEastAntartica.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')
CreaFigura(gcf,strcat(mfilename,'02'),[7])

%% Pacific
figure
m_proj('robinson','lon',[100 340]);
m_coast('patch',[.7 1 .7],'edgecolor','none'); hold on
m_grid

file=('./Cuencas/NPWest.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/NPEast.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/NPEastEast.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/NPCentral.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/SPCentral.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/SPWestCentral.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/SPEastAustralia.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/SIEastAntartica.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/SPWest.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/SPEastNorth.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/SPEastChile.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/SouthAustralia.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')

file=('./Cuencas/SPEastAntartica.csv');
D=readtable(file);
m_plot(D.lon,D.lat,'b','linewidth',3)
m_hatch(D.lon,D.lat,'single',-45,5,'color','k');
m_text(nanmean(D.lon),nanmean(D.lat),file(11:end-4),'HorizontalAlignment','center','BackgroundColor','w')
CreaFigura(gcf,strcat(mfilename,'03'),[7])
