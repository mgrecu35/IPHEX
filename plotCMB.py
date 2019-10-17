from readLinData import *
from   numpy import *
import matplotlib
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.colors as col
from matplotlib.colors import LogNorm
from matplotlib.ticker import LogLocator,LogFormatter
from matplotlib.colors import BoundaryNorm
from matplotlib.colors import LogNorm
import pickle

import glob
fCRSL=sorted(glob.glob('IPHEX/*CRS*'))
fKaL=sorted(glob.glob('IPHEX/*HKa*'))
fKuL=sorted(glob.glob('IPHEX/*HKu*'))

cfadz1=zeros((70,90),float)
cfadz2=zeros((70,90),float)
cfadz3=zeros((70,90),float)

def incCfad(z1L,h1,h0,k,cfad1):
    if z1L[k]>-5:
        i0=int((h1[k]-h0+1200)/125.)
        j0=int(z1L[k]/0.5)
        if i0>=0 and i0<70 and j0>=0 and j0<90:
            cfad1[i0,j0]+=1

h0=1000.

def onclick(event):
    global ix, iy
    ix, iy = event.xdata, event.ydata
    global coords
    coords = [ix, iy]
    print(coords)
    if iy>4:
        fig.canvas.mpl_disconnect(cid)
    hbbL.append(coords)
    return coords
import pickle
igetHBB=0


if1=0
zKuRL=[]
zKaRL=[]
z1L=[]
xL=[]



fs1=['Lin/iphex_comb_radar2014503_185703-190442.nc',\
     'Lin/iphex_comb_radar2014503_190645-192513.nc',\
     'Lin/iphex_comb_radar2014512_125511-130241.nc',\
     'Lin/iphex_comb_radar2014515_140811-142600.nc',
     'Lin/iphex_comb_radar2014515_142919-144814.nc,'\
     'Lin/iphex_comb_radar2014516_132703-133315.nc',
     'Lin/iphex_comb_radar2014523_222426-223201.nc',
     'Lin/iphex_comb_radar2014524_013152-014227.nc',
     'Lin/iphex_comb_radar2014524_014641-015700.nc',
     'Lin/iphex_comb_radar2014529_210445-210937.nc']

from netCDF4 import Dataset

fs=glob.glob('Lin/iphex_co*nc')
fs=sorted(fs)
ind=[490,100,900,1700,250,290,700,1100,900,400]
ip=0
dBaseL=[]
zXL=[]
zKuL=[]
zWL=[]
iplot=0
for f in fs[:]:
    if 'freq' in f:
        continue
    fh=Dataset(f)
    zku=fh['zku'][:,:]
    zx=fh['zx'][:,:]
    zka=fh['zka'][:,:]
    zw=fh['zw'][:,:]
    h=fh['altitude'][:]
    dist=fh['dist'][:]
    r=fh['range'][:]
    zkum=ma.array(zku,mask=zku<-10)
    zxm=ma.array(zx,mask=zx<-10)
    zkam=ma.array(zka,mask=zka<-10)
    zwm=ma.array(zw,mask=zw<-10)
    a=nonzero(zkum[:,120:400].sum(axis=1)>1000)
    for i in a[0]:
        dBaseL.append(zka[i,80:410:3])
        zXL.append(zx[i,80:410:3])
        zKuL.append(zku[i,80:410:3])
        zWL.append(zw[i,80:410:3])
    if iplot==1:
        plt.figure()
        plt.subplot(311)
        n=zxm.shape[0]
        d=arange(n)
        plt.pcolormesh(d,20-r[120:400],zkum[:,120:400].T,vmin=0,vmax=50,cmap='jet')
        plt.subplot(312)
        plt.pcolormesh(d,20-r,zkam.T,vmin=0,vmax=50,cmap='jet')
        plt.subplot(313)
        plt.pcolormesh(d,20-r,zwm.T,vmin=0,vmax=50,cmap='jet')
        stop
        #plt.figure()
    #plt.plot(zxm[ind[ip],:],20-r)
    #plt.plot(zkum[ind[ip],:],20-r)
    #plt.plot(zkam[ind[ip],:],20-r)
    #plt.plot(zwm[ind[ip],:],20-r)
    #plt.xlim(-10,50)
    ip+=1
    #    print(f)
    #plt.show()


from sklearn.cluster import MiniBatchKMeans
nc=70
h=20-r[80:410:3]
kmeans=MiniBatchKMeans(n_clusters=nc,batch_size=5000,random_state=0)
dBaseL=array(dBaseL)
dBaseL[dBaseL<-30]=-30
zXL=array(zXL)
zXL[zXL<-30]=-30
zKuL=array(zKuL)
zKuL[zKuL<-30]=-30
zWL=array(zWL)
zWL[zWL<-30]=-30
kmeans.fit(dBaseL[:,:-10])
#classes=[3,7,23,26,30,32,45,61,63,64,69]
classes=[4,8,11,12,22,23,25,36,40,53]
classes=[5,8,19,29,34,41,67,58]
import matplotlib

matplotlib.rcParams.update({'font.size': 13})
ic=1
nL=dBaseL.shape[0]
f1=0
for i in range(nc):
    if i+1 in classes:
        a=nonzero(kmeans.labels_==i)
        plt.figure()
        zc=dBaseL[a[0],:].mean(axis=0)
        zerr=dBaseL[a[0],:].std(axis=0)
        plt.errorbar(zc,h,xerr=zerr)
        
        plt.plot(zXL[a[0],:].mean(axis=0),h)
        plt.plot(zKuL[a[0],:].mean(axis=0),h)
        plt.plot(zWL[a[0],:].mean(axis=0),h)
        plt.legend(['X','Ku','W','Ka'])
        plt.xlabel('dBZ')
        plt.ylabel('Height (km)')
        plt.title("Convective Class %2.2i \n freq=%6.2f%%"%(ic,len(a[0])*100./nL))
        plt.xlim(-25,55)
        f1+=len(a[0])*100./nL
        ic+=1
        plt.savefig('class_2%2.2i.png'%i)
        
        
