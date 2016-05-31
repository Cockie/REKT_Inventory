from scipy import misc
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cbook import get_sample_data
from matplotlib.colors import LightSource
import matplotlib.cm as cm
import matplotlib.mlab as mlab

face = misc.imread('heightmap.png', flatten = True)

print(face)


z = face*1800./255-900
z=np.flipud(z)

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
'''

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


plt.show()'''

# Or you can use a colormap to specify the colors; the default
# colormap will be used for the contour lines
plt.figure()
im = plt.imshow(z, interpolation='bilinear', origin='lower',
                cmap=cm.terrain, extent=(-3, 3, -3, 3))
levels = np.arange(-900, 900, 100)
CS = plt.contour(z, levels,
                 origin='lower',
                 linewidths=1, extent=(-3, 3, -3, 3), cmap=cm.jet)

# Thicken the zero contour.
#zc = CS.collections[6]
#plt.setp(zc, linewidth=4)

plt.clabel(CS, levels[1::2],  # label every second level
           inline=1,
           fmt='%1.1f',
           fontsize=14)

# make a colorbar for the contour lines
#CB = plt.colorbar(CS, shrink=0.8, extend='both')

plt.title('Lines with colorbar')
#plt.hot()  # Now change the colormap for the contour lines and colorbar
plt.flag()

# We can still add a colorbar for the image, too.
# = plt.colorbar(im, orientation='horizontal', shrink=0.8)

# This makes the original colorbar look a bit out of place,
# so let's improve its position.

#l, b, w, h = plt.gca().get_position().bounds
#ll, bb, ww, hh = CB.ax.get_position().bounds
#CB.ax.set_position([ll, b + 0.1*h, ww, h*0.8])


plt.show()