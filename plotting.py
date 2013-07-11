
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
	
#===============================================================

def multi_hist_plot(table_object, *args, width, height):
	
	Nargs= len(args)
	
	figsize(width,height)
	
	fig, axes = subplots(Nargs)
	for ii in range(Nargs):
		axes[ii].hist(table_object[args(ii)],histtype='stepfilled')
		plt.xlabel(args(ii), fontsize=20)
	    savefig('fig'+str(args(ii))+'.png', transparent=True)
		
	fig.subplots_adjust(wspace=0.1, hspace=0.1)