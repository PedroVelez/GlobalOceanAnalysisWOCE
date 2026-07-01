close all
clear all

%%
Slongs=[-100 43;-75 20; 20 145;43 100;145 295;100 295];
Slats= [  0  90;-90  0;-90   0; 0  90;-90   0;  0  90];

l=5;
m_proj('mollweide','long',Slongs(l,:),'lat',Slats(l,:));
m_grid('fontsize',6,'xticklabels',[],'xtick',[-180:30:360],...
    'ytick',[-80:20:80],'yticklabels',[],'linest','-','color','k')
m_coast('patch',[.6 .6 .6]);hold on

D=readtable('./Cuencas/SPEastAntartica.csv');
m_plot(D.lon,D.lat,'b','linewidth',3)


l=2;
m_proj('mollweide','long',Slongs(l,:),'lat',Slats(l,:));
m_grid('fontsize',6,'xticklabels',[],'xtick',[-180:30:360],...
    'ytick',[-80:20:80],'yticklabels',[],'linest','-','color','k')
m_coast('patch',[.6 .6 .6]);hold on

D=readtable('./Cuencas/SAWestNorth_Incompleta.csv');
m_plot(D.lon,D.lat,'b','linewidth',3)
m_plot(D.lon(1),D.lat(1),'bo','linewidth',3)

