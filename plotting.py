
#=======================================================================#

import numpy as np
from utilities import FitsTable
import matplotlib.pylab as plt
import pdb

#=======================================================================#
#
#
#def HistPlot (x,y,binsize=10):
#
#	# initialize figure and axes
	#fig = plt.figure()
	#axes = fig.add_subplot(111)

	# initialize some parameters for the plot
	
	# the x bounds
	#xmin = np.min(x)
	#xmax = np.max(x)

	# the bin edges based on the bin size
	#bins = np.arange(xmin,xmax,binsize)
	
	# plot parameters
	#axes.set_xlim(xmin,xmax)
	
#===============================================================

def multi_hist_plot(table_object, width, height, *args):
	if not isinstance(table_object,FitsTable):
		raise TypeError("that bad")
		
	# how many plots
	Nargs= len(args)
	
	# initialize the figures and axes
	fig, axes = plt.subplots(Nargs)
	# if only one plot then make a list
	if Nargs == 1:
		axes = [axes]
	
	# loop over all the axes
	for ii in range(Nargs):
		# plot the histogram on the axes
		axes[ii].hist(table_object[args[ii]])#histtype='stepfilled')
		# set the xlabel
		axes[ii].set_xlabel(args[ii], fontsize=20)
	
	# adjust whitespace
	fig.subplots_adjust(wspace=0.1, hspace=0.1)
	# save
	fig.savefig('figures.png', transparent=True)
	