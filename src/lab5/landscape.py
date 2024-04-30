import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import numpy as np
import random as rd

def get_elevation(size):
    xpix, ypix = size
    elevation = np.array([])
    noise = PerlinNoise(octaves=5, seed =rd.randint(0,1000))
    xpix,ypix = size[0],size[1]
    elevation =np.array([[noise([i/xpix, j/ypix])
                          for j in range(ypix)]
                            for i in range(xpix)]
                        )

    '''Play around with perlin noise to get a better looking landscape (This is required for the lab)'''

    return np.array(elevation)

def elevation_to_rgba(elevation, cmap='terrain_r'):
    xpix, ypix = np.array(elevation).shape
    colormap = plt.cm.get_cmap(cmap)
    elevation = (elevation - elevation.min())/(elevation.max()-elevation.min())
    ''' You can play around with colormap to get a landscape of your preference if you want '''
    landscape = np.array([colormap(elevation[i, j])[0:3] for i in range(xpix) for j in range(ypix)]).reshape(xpix, ypix, 3)*255
    landscape = landscape.astype('uint8')
    return landscape
 

get_landscape = lambda size: elevation_to_rgba(get_elevation(size))

if __name__ == '__main__':
    size = 640, 480
    pic = elevation_to_rgba(get_elevation(size))
    plt.imshow(pic, cmap='terrain_r')
    plt.show()