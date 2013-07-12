import os
from astropy.io import fits
import numpy as np
import sys
from glob import glob


class FitsTable (object):
	
    def __init__(self, filepath, fix_nan=None):
		
        # check that the file exists
        if not os.path.isfile(filepath):
            raise IOError("File does not exist :"+str(filepath))
            
  		# filepath
        self.filepath = os.path.abspath(filepath) 
        
        # open the fits file
        self.hdulist = fits.open(self.filepath, memmap=False)

        # table header
        self.header = self.hdulist[1].header

        # store the nan value you want to fix
        self.fix_nan = fix_nan

        # initialize the columns and numbers
        self.columns = self.hdulist[1].columns.names
        
        self.flag = np.zeros(self.hdulist[1].data.field('FLAG').shape)
        self.flag[self.hdulist[1].data.field('FLAG') == 'nnnnn'] = 1.

    def _fix_nan_values(self,arr):
        if self.fix_nan is None: 
            return arr
        else:
            arr[arr == self.fix_nan] = np.NaN
            return arr
            
    def __getitem__(self,column):
        """ Accessing columns"""

        if column in self.columns and type(column) == str:
            self.hdulist[1].data.field(column)[self.flag == 0] = np.nan
            return np.array(self.hdulist[1].data.field(column))



def ivar_2_var (ivar,fill=1e50):
    ivar = np.array(ivar,dtype=float)
    zeros = (ivar == 0.0)
    bad = (ivar >= fill)
    ivar[zeros] = -1.0
    var = 1.0/ivar
    var[zeros] = fill
    var[bad] = 0.0
    return var

def var_2_ivar (var,fill=1e50):
    var = np.array(var,dtype=float)
    zeros = (var==0)
    bad = (var>=fill/2.0)
    
    var[zeros] = -1.0
    ivar = 1.0/var
    
    # set points which are very large to the fill
    ivar[zeros] = fill
    # set points which are almost zero to zero
    ivar[bad] = 0.0

    return ivar


def download_sdss_file (plate,fiber,mjd,output_path=None):
    # set url path to the data
    url_path = "http://api.sdss3.org/spectrum?"
    url_path += "plate="+str(plate)
    url_path += "&fiber="+str(fiber)
    url_path += "&mjd="+str(mjd)
    
    # execute the commands for the files
    cmd = "wget --content-disposition '"+url_path+"'"
    #cmd = "wget '"+url_path+"'"
    print("Gave command$ "+cmd)
    os.system(cmd)

    cmd = "curl --remote-header-name -O '"+url_path+"'"
    # cmd = "curl -O '"+url_path+"'"
    print("Gave command$ "+cmd)
    os.system(cmd)

    lookfor = "*".join(("spec",
                        str(plate),
                        str(mjd),
                        str(fiber),
                        ))+".fits"

    filename_list = glob(lookfor)
 
    # check filename
    if len(filename_list) ==0:
        raise IOError("File from the SDSS site was not give expected filename:"+_lookfor+"   "+str(filename_list))
    
    filepath = os.path.abspath(filename_list[0])
    
    if output_path is not None:
        if os.path.exists(output_path) and not clobber:
            raise IOError("File already exists: "+str(output_path))
        os.system("mv "+filepath+"  "+output_path)

    filepath = os.path.abspath(filepath)
    return filepath


class Spectrum (object):   
    def __init__ (self,wavelengths,flux,ivar=None):
        """
        """
        # get the wavelengths and flux and check that they match
        self.wavelengths = np.asarray(wavelengths)
        self.flux = np.asarray(flux)
        if self.wavelengths.shape != self.flux.shape: 
            raise ValueError("wavelength and flux shapes do not match")

        # store shape
        self.shape = wavelengths.shape

        # get inverse variance
        if ivar is None:
            self.ivar = np.ones_like(wavelengths)
        else:
            self.ivar = np.asarray(ivar)
            if self.ivar.shape != self.shape:
                raise ValueError("inverse varience does not have same shape as data")

    def _check_spectrum_instance (self,spec):
        if not isinstance(spec,SDSS_Spectrum):
            raise TypeError("Can't + this to current SDSS_Spectrum : "+type(spec))

    def __eq__ (self,spec):
        self._check_spectrum_instance(spec)
        c1 = np.all(spec.wavelengths == self.wavelengths)
        c2 = np.all(spec.flux == self.flux)
        c3 = np.all(spec.ivar == self.ivar)
        return c1 and c2 and c3

    def __add__ (self,spec):
        self._check_spectrum_instance(spec)

        flux = (self.flux*self.ivar+spec.flux*spec.ivar)/(sum(self.ivar+spec.ivar))
        ivar = var_2_ivar(ivar_2_var(self.ivar)+ivar_2_var(spec.ivar))
        
        return Spectrum(self.wavelengths,flux,ivar)


class SDSS_Spectrum (Spectrum):
    
    def __init__ (self,plate,fiber,mjd):
        """
        
        This takes the plate, fiber, and mjd to the SDSS api to download that file using

        wget --content-disposition http://api.sdss3.org/spectrum?plate=0000&fiber=000000&mj0000
        curl --remote_header_name -O http://api.sdss3.org/spectrum?plate=0000&fiber=000000&mj0000

        if filepath is given then it will use os.system to move that file to the location

        """
        # check that inputs are integers
    	plate = int(plate)
    	fiber = int(fiber)
    	mjd = int(mjd)

        self.sdss_identify = {"plate":plate,
                              "fiber":fiber,
                              "mjd":mjd}

        # create the file from the format
    	lookfor = "*".join(("spec",
                            str(self.sdss_identify["plate"]),
                            str(self.sdss_identify["mjd"]),
                            str(self.sdss_identify["fiber"]),
                            ))+".fits"

        filename_list = glob(lookfor)

        # if file doesn't exist here then download it
        if len(filename_list) == 0:
            self.filepath = download_sdss_file(plate,fiber,mjd)
        else:
            self.filepath = os.path.abspath(filename_list[0])

        # open the file with fits
        self.hdulist = fits.open(self.filepath,ignore_missing_end=True)

        # get the header information
        self.primary_header = self.hdulist[0].header
        self.data_header = self.hdulist[1].header

        # get the data
        flux = self.hdulist[1].data['flux']
        wavelengths = 10**(self.hdulist[1].data['loglam'])
        ivar = self.hdulist[1].data['ivar']

        super(SDSS_Spectrum,self).__init__(wavelengths,flux,ivar)


    def move_file (self,filepath,clobber=True):
        if os.path.exists(filepath) and not clobber:
            raise IOError("File already exists: "+str(filepath))
        os.system("mv "+self.filename+"  "+filepath)
        self.filename = os.path.abspath(filepath)
