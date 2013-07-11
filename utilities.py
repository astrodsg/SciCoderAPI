import os
from astropy.io import fits
import numpy as np
import sys
import glob


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
        	# self.hdulist[1].data.field(column)[self.flag == 0] = np.nan
        	return np.array(self.hdulist[1].data.field(column))



















# get the entire header 
# keyword == TTYPE*
# keyword get the column number
# get the column label

        
        
