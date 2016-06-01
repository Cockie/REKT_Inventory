from scipy import misc
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cbook import get_sample_data
from matplotlib.colors import LightSource
import matplotlib.cm as cm
import matplotlib.mlab as mlab

face = misc.imread('heightmap.png', flatten=True)

z = face * 1800. / 255 - 1000
zmin = min(z.ravel())
zmax = max(z.ravel())
unit = 1024 / 10
xmin = 5
xmax = 10
ymin = 5
ymax = 10
dx = round((xmax - xmin))
dy = round((ymax - ymin))
#print(dx, dy)
z = z[int(ymin * unit):int(ymax * unit), int(xmin * unit):int(xmax * unit)]

# Or you can use a colormap to specify the colors; the default
# colormap will be used for the contour lines
plt.figure()
im = plt.imshow(z, interpolation='bilinear', origin='lower',
                cmap=cm.terrain, extent=(0, dx, 0, dy), vmin=zmin, vmax=zmax)
levels = np.arange(round(min(z.ravel()), -1), round(max(z.ravel()), -1), 100)
CS = plt.contour(z, levels,
                 origin='lower',
                 linewidths=1, extent=(0, dx, 0, dy), cmap=plt.get_cmap('jet'))

circle1 = plt.Circle((2 - xmin, 5 - ymin), 2, edgecolor='#ee00ff', facecolor='none', linewidth=3)
circle2 = plt.Circle((2.5 - xmin, 0.7 - ymin), 1.5, edgecolor='#0055ff', facecolor='none', linewidth=3)
circle3 = plt.Circle((2.5 - xmin, 1 - ymin), 9.5, edgecolor='#660099', facecolor='none', linewidth=2)
circle4 = plt.Circle((3.5 - xmin, 3.2 - ymin), 2, edgecolor='#ee00ff', facecolor='none', linewidth=3)
circle5 = plt.Circle((1.4 - xmin, 5.9 - ymin), 4.1, edgecolor='#aa00cc', facecolor='none', linewidth=2)
circle6 = plt.Circle((5.3 - xmin, 3.5 - ymin), 4, edgecolor='#aa00cc', facecolor='none', linewidth=2)
plt.gcf().gca().add_artist(circle1)
plt.gcf().gca().add_artist(circle2)
plt.gcf().gca().add_artist(circle3)
plt.gcf().gca().add_artist(circle4)
plt.gcf().gca().add_artist(circle5)
plt.gcf().gca().add_artist(circle6)

# Thicken the zero contour.
# zc = CS.collections[6]
# plt.setp(zc, linewidth=2)

plt.clabel(CS, levels[1::2],  # label every second level
           inline=1,
           fmt='%1.1f',
           fontsize=14)

# make a colorbar for the contour lines
# CB = plt.colorbar(CS, shrink=0.8, extend='both')

plt.title("Sitatha's Canyons - Topographical Map")
#plt.jet()  # Now change the colormap for the contour lines and colorbar
plt.flag()

# We can still add a colorbar for the image, too.
# CB = plt.colorbar(im, orientation='horizontal', shrink=0.8)

# This makes the original colorbar look a bit out of place,
# so let's improve its position.

# l, b, w, h = plt.gca().get_position().bounds
# ll, bb, ww, hh = CB.ax.get_position().bounds
# CB.ax.set_position([ll, b + 0.1*h, ww, h*0.8])

plt.xticks(np.arange(0, dx + 1, 1.0))
plt.yticks(np.arange(dy, -1, -1.0))
plt.gca().invert_yaxis()
plt.grid(True)
plt.show()
