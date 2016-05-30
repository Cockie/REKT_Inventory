from scipy import misc
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cbook import get_sample_data
from matplotlib.colors import LightSource

face = misc.imread('heightmap.png', flatten = True)

print(face)


z = face

#-- Optional dx and dy for accurate vertical exaggeration --------------------
# If you need topographically accurate vertical exaggeration, or you don't want
# to guess at what *vert_exag* should be, you'll need to specify the cellsize
# of the grid (i.e. the *dx* and *dy* parameters).  Otherwise, any *vert_exag*
# value you specify will be realitive to the grid spacing of your input data
# (in other words, *dx* and *dy* default to 1.0, and *vert_exag* is calculated
# relative to those parameters).  Similarly, *dx* and *dy* are assumed to be in
# the same units as your input z-values.  Therefore, we'll need to convert the
# given dx and dy from decimal degrees to meters.
#-----------------------------------------------------------------------------

ls = LightSource(azdeg=315, altdeg=45)
cmap = plt.cm.RdPu

fig, axes = plt.subplots(nrows=1, ncols=1)
#plt.setp(axes.flat, xticks=[], yticks=[])

# Vary vertical exaggeration and blend mode and plot all combinations
    # Show the hillshade intensity image in the first row
plt.imshow(ls.hillshade(z, vert_exag=5), cmap='gray')
    # Place hillshaded plots with different blend modes in the rest of the rows
    #for ax, mode in zip(col[1:], ['hsv', 'overlay', 'soft']):
rgb = ls.shade(z, cmap=cmap, blend_mode='soft',
                       vert_exag=5, range=(0,300))
plt.imshow(rgb)


plt.show()