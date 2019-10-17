from numpy import *
from scipy.io import netcdf as cdf
from netCDF4 import Dataset
def readKu(fname,n1):
    f=Dataset(fname,'r')
    r=f.variables['range'][n1:]
    zku=f.variables['zku'][:,n1:]
    vku=f.variables['dopcorr'][:,n1:]
    lat=f.variables['lat'][:]
    lon=f.variables['lon'][:]
    alt=f.variables['altitude'][:]
    roll=f.variables['roll'][:]
    t=f.variables['timed'][:]
    return zku,lat,lon,r,alt,roll,t, vku

def readKa(fname,n1):
    f=Dataset(fname,'r')
    r=f.variables['range'][n1:]
    zku=f.variables['zku'][:,n1:]
    lat=f.variables['lat'][:]
    lon=f.variables['lon'][:]
    alt=f.variables['altitude'][:]
    roll=f.variables['roll'][:]
    vku=f.variables['dopcorr'][:,n1:]
    return zku,lat,lon,r,alt,roll

def readiphex(fname):
    f=Dataset(fname,'r')
    r=f.variables['range'][:]
    dist=f.variables['dist'][:]
    zx=f.variables['zx'][:,:]
    zka=f.variables['zka'][:,:]
    zku=f.variables['zku'][:,:]
    
    vx=f.variables['dopx'][:,:]
    vku=f.variables['dopku'][:,:]
    vka=f.variables['dopka'][:,:]
    vw=f.variables['dopw'][:,:]
    zw=f.variables['zw'][:,:]
    zx=zx-0.5
    lat=f.variables['lat'][:]
    lon=f.variables['lon'][:]
    alt=f.variables['altitude'][:]
    return zx,zka,zku,zw,vx,vku,vka,vw,lat,lon,r,alt,dist

def readiphexX(fname):
    f=Dataset(fname,'r')
    r=f.variables['range'][:]
    zku=f.variables['zku'][:,:]
    lat=f.variables['lat'][:]
    lon=f.variables['lon'][:]
    alt=f.variables['altitude'][:]
    return zku,lat,lon,r,alt
