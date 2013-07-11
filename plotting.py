
#=======================================================================#

import numpy as np
from .utilities import FitsTable
import matplotlib.pylab as plt


#=======================================================================#
#

def HistPlot (x,y,binsize=10):

	# initialize figure and axes
	fig = plt.figure()
	axes = fig.add_subplot(111)

	# initialize some parameters for the plot
	
	# the x bounds
	xmin = np.min(x)
	xmax = np.max(x)

	# the bin edges based on the bin size
	bins = np.arange(xmin,xmax,binsize)
	
	# plot parameters
	axes.set_xlim(xmin,xmax)

	
