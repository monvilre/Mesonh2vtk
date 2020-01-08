from netCDF4 import Dataset
import numpy as np
from pyevtk.hl import gridToVTK
import os
def field2vtk(files,var):
    for fi in range(len(files)):
        
        ncfile1 = Dataset(files[fi],'r')
        variab = [None]*len(var)
        for j in range(len(var)):
            v = ncfile1.variables[var[j]][0,:,:,:] 
            vv = np.rot90(np.float64(v),1,(2,0))[1:,1:,:v.shape[0]-1]
            variab[j] = np.copy(vv, order = 'F')
        IIE=variab[0].shape[0]+1
        IJE=variab[0].shape[1]+1
        IKE=variab[0].shape[2]+1  
        Z=ncfile1.variables["ZHAT"][:]
        H = np.max(Z)
        ALT=np.zeros((IKE-1,IJE,IIE),dtype='f')
        ZS=ncfile1.variables['ZS'][:,:]
        for k in range(1,IKE):
            ALT[k-1,:,:]= (1-(ZS[:,:]/H))*Z[k]+ZS[:,:]
        Y = ncfile1.variables['YHAT'][:].data
        X = ncfile1.variables['XHAT'][:].data
        x= np.zeros((IKE-1,len(X),len(Y)))
        y= np.zeros((IKE-1,len(X),len(Y)))
        y[0,:,:],x[0,:,:] =np.meshgrid(X,Y)
        
        for i in range(IKE-1):
            x[i,:,:] = x[0,:,:]
            y[i,:,:] = y[0,:,:]
        z = np.float64(ALT)[:,:,:]
        x = np.rot90(np.float64(x),1,(2,0))[1:,1:,:]
        y = np.rot90(np.float64(y),1,(2,0))[1:,1:,:]
        z = np.rot90(np.float64(z),1,(2,0))[1:,1:,:]
        z = np.copy(z, order = 'F')
        x = np.copy(x, order = 'F')
        y = np.copy(y, order = 'F')
        data = dict(zip(var,variab))
        na = os.path.split(files[fi])[-1][:-3]
        gridToVTK(na,y,x,z, pointData = data)
        print(na)

def MNT(file):
    hi = 2
    ncfile1 = Dataset(file,'r')
    ZS=ncfile1.variables['ZS'][:,:]
    Y = ncfile1.variables['YHAT'][:].data
    X = ncfile1.variables['XHAT'][:].data
    IIE=len(X)
    IJE=len(Y)

    x= np.zeros((hi,len(X),len(Y)))
    y= np.zeros((hi,len(X),len(Y)))
    x[0,:,:],y[0,:,:] =np.meshgrid(X,Y)
    for i in range(hi):
        x[i,:,:] = x[0,:,:]
        y[i,:,:] = y[0,:,:]
    x = np.rot90(np.float64(x),1,(2,0))[1:,1:,:]
    y = np.rot90(np.float64(y),1,(2,0))[1:,1:,:]
    x = np.copy(x, order = 'F')
    y = np.copy(y, order = 'F')
    
    z0= np.zeros((len(X),len(Y)))
    
    z = np.linspace(z0,ZS,hi).data
    Z = np.rot90(np.float64(z),1,(2,0))[1:,1:,:]
    Z = np.copy(Z, order = 'F')
    na = os.path.split(file)[-1][:-3]
    gridToVTK('./MNT'+ na,x,y,Z, pointData = {"Z": Z})
    print(na + 'MNT')
