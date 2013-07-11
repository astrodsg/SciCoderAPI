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
<<<<<<< HEAD
        if self.fix_nan is None: return arr
        arr[arr == self.fix_nan] = np.NaN
        return arr

    
=======
		if self.fix_nan is None: 
			return arr
		else:
			arr[arr == self.fix_nan] = np.NaN
			return arr
            
>>>>>>> 2fce7b54df00ee9ab5aa22dc4a6f2ab10d439f12
    def __getitem__(self,column):
        """ Accessing columns"""

        if column in self.columns and type(column) == str:
        	# self.hdulist[1].data.field(column)[self.flag == 0] = np.nan
        	return np.array(self.hdulist[1].data.field(column))


class SDSS_Spectrum (object):
    
    def __init__ (self,plate,fiber,mjd,filepath='.'):
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
    	
        self.identify = {"plate":plate,
                         "fiber":fiber,
                         "mjd":mjd}

        # create the file from the format
    	self._lookfor = "*".join(("spec",
                                  str(self.identify["plate"]),
                                  str(self.identify["mjd"]),
                                  str(self.identify["fiber"]),
                                  ))+".fits"
        filename_list = glob(self._lookfor)

        # if file doesn't exist here then download it
        # todo: check the filepath location for the file
        if len(filename_list) == 0:
            filename_list = self._download_file(plate,fiber,mjd)
        else:
            self.filepath = os.path.abspath(filename_list[0])
            
        # open the file with fits
        self.hdulist = fits.open(self.filepath,ignore_missing_end=True)

        # move the file to another location
        # todo: implement
        #os.system("mv "+self.filename+

<<<<<<< HEAD
        # get the header information
        self.primary_header = self.hdulist[0].header
        self.data_header = self.hdulist[1].header
=======















# get the entire header 
# keyword == TTYPE*
# keyword get the column number
# get the column label

>>>>>>> 2fce7b54df00ee9ab5aa22dc4a6f2ab10d439f12
        
        # get the data
        self.flux = self.hdulist[1].data['flux']
        self.wavelength = 10**(self.hdulist[1].data['loglam'])


    def _download_file (self,plate,fiber,mjd):
        # set url path to the data
    	self.url_path = "http://api.sdss3.org/spectrum?"
    	self.url_path += "plate="+str(plate)
    	self.url_path += "&fiber="+str(fiber)
    	self.url_path += "&mjd="+str(mjd)
		    
	cmd = "wget --content-disposition '"+self.url_path+"'"
        #cmd = "wget '"+self.url_path+"'"
        print("Gave command$ "+cmd)
        os.system(cmd)

        cmd = "curl --remote-header-name -O '"+self.url_path+"'"
        #cmd = "curl -O '"+self.url_path+"'"
        print("Gave command$ "+cmd)
        os.system(cmd)
        
        filename_list = glob(self._lookfor)

        # check filename
        if len(filename_list) ==0:
            raise IOError("File from the SDSS site was not give expected filename:"+self._lookfor+"   "+str(filename_list))

        self.filepath = filename_list[0]
