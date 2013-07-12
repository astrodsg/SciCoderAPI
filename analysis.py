import astropy.units as u
import numpy as np
import numpy.lib.recfunctions as nprec



def cel_to_cart (l,b,d):
    gx,gy,gz = _math_for_cel_to_cart(l,b,d)
    arr = np.array([tuple(gx),tuple(gy),tuple(gz)],
		    dtype=[('Gx',float),('Gy', float),('Gz',float)] 
    return arr

def _math_for_cel_to_cart(Glon_deg, Glat_deg, heliod_noUnit):
	
	Glon=Glon_deg*180/np.pi
	Glat=Glat_deg*180/np.pi
	
	heliod=1000*heliod_noUnit*u.pc
	
	Gx= heliod*np.cos(Glon)*np.sin(Glat)-8500*u.pc
	Gy= heliod*np.sin(Glat)*np.sin(Glon)
	Gz= heliod*np.cos(Glat)
	
	return Gx Gy Gz
	
#============================================================


  
  
  