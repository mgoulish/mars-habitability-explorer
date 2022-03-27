import glob
import logging
import os
import netCDF4
import numpy as np


# Set up a logger
level = logging.INFO
log = logging.getLogger(__name__)
log.setLevel(level)


def reduce_data(file_path, variable):
    """
    Calculate the average of a netcdf file.

    :param file_path: Path to the netcdf file.
    :param variable: Variable to calculate the average.

    :return: Average of the netcdf variable.
    """
    file_list = glob.glob(os.path.join(file_path, 'openmars*.nc'))

    data_list = []
    for fil in file_list:
        log.debug('Reading file: {}'.format(fil))
        with netCDF4.Dataset(fil, 'r') as nc_file:
            data = nc_file.variables[variable]
            log.debug(data)

            # Average over the time dimension for each dataset
            if data.DEPEND_0 == 'time':
                log.debug('Found time dimension')
                # We only care about ground level so take bottom
                # if there are multiple levels
                if data.DEPEND_1 == 'lev':
                    log.debug('Found level dimension')
                    data_list.append(np.average(data[:,0,:,:], axis=0))
                else:
                    log.debug('Found no level dimension')
                    data_list.append(np.average(data[:,:,:], axis=0))
    stats = {'avg': np.average(data_list, axis=0),
             'median': np.median(data_list, axis=0),
             'max': np.amax(data_list, axis=0),
             'min': np.amin(data_list, axis=0),
             'std': np.std(data_list, axis=0)}

    return stats


def average_all(file_path):
    """
    average over all of the variables in an OpenMars file

    :param file_path: Path to the netcdf files for OpenMars.

    :return: stats on all of the files found in OpenMars.
    """

    # Use the keys to iterate over the data we want to aggrigate
    data = {'ps':{},
            'tsurf': {},
            'dustcol': {},
            'u': {},
            'v': {}
            }

    for var in data.keys():
        log.debug('Working on variable: {}'.format(var))
        data[var] = reduce_data(file_path, var)

    return data


def new_file(file_path, data, file_name='avg_openmars.nc'):
    """
    Aggrigates data from the openMars dataset
        
    :param file_path: Path to the netcdf files for OpenMars.
    :param file_name: Name of the new netcdf file.
    :param data: Dictionary of the data to be written to the new file.

    """
    # Datums to put into the file
    dataum_to_use = ['avg', 'median', 'max', 'min', 'std']
    # Units to put into the groups
    units = {'ps': 'Pa',
            'tsurf': 'K',
            'dustcol': 'NU',
            'u': 'm/s',
            'v': 'm/s'
            }

    # Get the lat and long of one of the OpenMars files
    files = glob.glob(os.path.join(file_path, 'openmars*.nc'))
    log.info('Reading file: {}'.format(files[0]))
    with netCDF4.Dataset(files[0], 'r') as nc_file:
        lat = nc_file.variables['lat']
        lon = nc_file.variables['lon']

        #log.debug(lat)
        #log.info('Succussfully read in lat and long. Creating new netcdf file.')

        # Create the new netcdf file
        filename = os.path.join(file_path, file_name)
        with netCDF4.Dataset(filename, 'w', format='NETCDF4') as f:
            f.createDimension('lat', lat.shape[0])
            f.createDimension('lon', lon.shape[0])
            latitude = f.createVariable('lat', 'f4', ('lat',))
            longitude = f.createVariable('lon', 'f4', ('lon',))
            latitude[:] = lat[:]
            longitude[:] = lon[:]
            log.info(f)
            for var in data.keys():
                grp = f.createGroup(var)
                latitude = grp.createVariable('lat', 'f4', ('lat',))
                longitude = grp.createVariable('lon', 'f4', ('lon',))
                latitude[:] = lat[:]
                longitude[:] = lon[:]
                for datum in dataum_to_use:
                    v = grp.createVariable(datum, 'f4', ('lat', 'lon'))
                    v.units = units[var]
                    log.debug("Data: {}".format(data[var][datum]))
                    v[:] = data[var][datum]
                    log.debug(v)
            log.info(f)


def do_all(file_path):
    """
    Do all of the steps to create a new netcdf file.

    :param file_path: Path to the netcdf files for OpenMars.

    """
    log.info('Starting average_all')
    data = average_all(file_path)

    log.info('Starting new_file')
    new_file(file_path, data)


def plot(lon, lat, stats, var, title=None):
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(14, 8))
    CS1 = plt.contourf(lon, lat, stats[var], 30, cmap = plt.cm.magma)
    cbar = plt.colorbar(CS1)
    plt.xticks(np.arange(-135,180,45), ('135$^\circ$W','90$^\circ$W','45$^\circ$W','0$^\circ$','45$^\circ$E','90$^\circ$E','135$^\circ$E'), fontsize=16 )
    plt.xlabel(r'Longitude', fontsize=18)
    plt.yticks( np.arange(-60,90,30), ('60$^\circ$S','30$^\circ$S','0$^\circ$','30$^\circ$N','60$^\circ$N'), fontsize=16  )
    plt.ylabel('Latitude', fontsize=18)
    plt.axis([-180., 175. -87.5, 87.5])
    if not title:
        plt.title(var, fontsize=20)
    else:
        plt.title(title, fontsize=20)
    plt.show()
