from ReadOriginalData import *


def locate(
        value: float,
        array : np.ndarray
) -> int:
    """
    Return index from the array's element closest to value.

    :param value: float to search
    :param array: array in which to search
    :return: array index
    """
    dist = abs(value - array)
    index = np.argmin(dist)
    return index


def occupation_matrix(
        ds : xr.Dataset,
        profile_idxs : list,
        latitudes : np.ndarray,
        longitudes : np.ndarray,
        depth : int,
        p_resolution : int = None
):
    """
    Compute array with shape (lats, lons, depth) that contains all the profiles in each latitude and longitude

    :param ds: xr dataset
    :param idxs: indexes to run
    :param latitudes: numpy array with values of latitudes
    :param longitudes: numpy array with values of longitudes
    :param depth: depth of the array (possible maximum of profiles in (lat, lon))
    :return: numpy array with occupations
    """
    p = ds.P.values.astype(int)
    pressures = np.arange(p[0], p[-1] + p_resolution, p_resolution, dtype = int)
    prof_ocupation = np.full((len(latitudes), len(longitudes), depth), np.nan)
    t_means = np.full((len(latitudes), len(longitudes), depth), np.nan)
    sal_means = np.full((len(latitudes), len(longitudes), depth), np.nan)
    times = np.full((len(latitudes), len(longitudes), depth), np.datetime64("NaT"), dtype = "datetime64[ns]") # Especifica que están las fechas en ns
    n = np.zeros((len(latitudes), len(longitudes)))
    for prof in profile_idxs: 
        if np.isnan(ds.latitude.values[prof]) == True or np.isnan(ds.longitude.values[prof]) == True: continue 

        ds.latitude.values[prof] = ds.latitude.values[prof] - 90 if ds.latitude.values[prof] > 90 else ds.latitude.values[prof]
        ds.longitude.values[prof] = ds.longitude.values[prof] - 180 if ds.longitude.values[prof] > 180 else ds.longitude.values[prof]

        ilat = locate(ds.latitude.values[prof], latitudes) 
        ilon = locate(ds.longitude.values[prof], longitudes)

        nans = np.where(np.isnan(prof_ocupation[ilat, ilon, :]) == True)
        not_nan_index = np.min(nans)
        prof_ocupation[ilat, ilon, not_nan_index] = prof
        n[ilat, ilon] += 1

        t = ds.ctd_temperature_filt[prof].values
        t_mean = np.mean(t)
        t_means[ilat, ilon, not_nan_index] = t_mean

        sal = ds.ctd_salinity_filt[prof].values
        sal_mean = np.mean(sal)
        sal_means[ilat, ilon, not_nan_index] = sal_mean


        time = ds.time[prof].values
        times[ilat, ilon, not_nan_index] = time

        
    n[np.where(n == 0)] = np.nan
    return (n, prof_ocupation, t_means, sal_means, times)