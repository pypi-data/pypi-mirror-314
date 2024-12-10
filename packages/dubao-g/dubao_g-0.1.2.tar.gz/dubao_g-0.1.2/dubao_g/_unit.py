import numpy as np
from datetime import timedelta
import datetime
from netCDF4 import Dataset
from netCDF4 import Dataset,date2num
from numpy import array,asarray,arange,flipud,dtype
def RYScaler(X_dbz):
	X_dbz[X_dbz < 0] = 0
	c1 = X_dbz.min()
	c2 = X_dbz.max()
	return ((X_dbz - c1) / (c2 - c1) * 255).astype(np.uint8), c1, c2
def inv_RYScaler(X_scl, c1, c2):
	X_scl = (X_scl / 255)*(c2 - c1) + c1
	return X_scl

def fixtime(timein='yyyyddmmHHMM',minutes_chose=10,formatcovert='%Y%m%d%H%M'):
	timein_obj  = datetime.datetime.strptime(timein, "%Y%m%d%H%M")
	utc_minus_7 = timein_obj + timedelta(minutes=minutes_chose)
	return utc_minus_7.strftime(formatcovert)


def readfile(filenc):
	fh = Dataset(filenc, mode='r')
	datanc={}
	for key in fh.variables.keys():
		datanc[key]=fh.variables[key][:]
	fh.close()
	return datanc
def soprint(x):
	if x<10:
		return f'00{x}'
	elif (x>=10) and (x<100):
		return f'0{x}'
	else:
		return f'00{x}'
def readmask(file_in):
	fh = Dataset(file_in, mode='r+')
	data=fh.variables['data'][:]
	lon=fh.variables['longitude'][:]
	lat=fh.variables['latitude'][:]
	return data, lon, lat