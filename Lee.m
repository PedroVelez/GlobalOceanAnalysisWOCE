dataDir='GoShip';

files=dir(strcat('./',dataDir,'/*.nc'));




figure; hold on
for ic=1:length(files)
    file=fullfile('GoShip',files(ic).name);
    ncid=netcdf.open(file,'nc_nowrite');

    try
        ID = netcdf.inqVarID(ncid,'ctd_temperature');
        
        lon=netcdf.getVar(ncid,netcdf.inqVarID(ncid,'longitude'));
        lat=netcdf.getVar(ncid,netcdf.inqVarID(ncid,'latitude'));
        plot(lon,lat,'o')
        
        section_id=ncread(file,'section_id')';
        expocode=ncread(file,'expocode')';
        
        fprintf('  > %12s %20s',section_id(1,:),expocode(1,:))
        fprintf(' %s',ncreadatt(file,'ctd_temperature','whp_unit'))
        fprintf('\n')

        [dimname, dimlen] = netcdf.inqDim(ncid,0)

    catch exception
        if strcmp(exception.identifier,'MATLAB:imagesci:netcdf:libraryFailure')
            str = 'bad';
        end
    end

end

