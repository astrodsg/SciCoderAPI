import astropy.units as u
import numpy as np


def cel_to_cart(Glon_deg, Glat_deg, heliod_noUnit):
	
	Glon=Glon_deg*180/np.pi
	Glat=Glat_deg*180/np.pi
	
	heliod=1000*heliod_noUnit*u.pc
	
	Gx= heliod*np.cos(Glon)*np.sin(Glat)-8500*u.pc
	Gy= heliod*np.sin(Glat)*np.sin(Glon)
	Gz= heliod*np.cos(Glat)
	
	R=[Gx,Gy,GZ]
	
	return R