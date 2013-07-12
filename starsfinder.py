def starsfinder(table_object, coords, width, height):
	
	if not isinstance(table_object,FitsTable):
		raise TypeError("No data")
		
	if ((coords[0]+width>90) | (coords[0]-width<-90) | (coords[1]+width>180) | (coords[1]+width<0)):
		raise TypeError("Out of the Sky")

		
	masklw=((table_object[coords[0]]+width)&(table_object[coords[0]]-width))
	masklh=((table_object[coords[1]]+height)&(table_object[coords[1]]-height))
	
	set_of_stars=(masklw,maskln) 
	return set_of_stars