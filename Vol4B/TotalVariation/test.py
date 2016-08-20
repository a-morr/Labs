from numpy.random import random_integers, uniform, randn
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.misc import imread, imsave

imagename = 'baloons_resized_bw.jpg'
changed_pixels=10000
# Read the image file imagename into an array of numbers, IM
# Multiply by 1. / 255 to change the values so that they are floating point
# numbers ranging from 0 to 1.
IM = imread(imagename, flatten=True) * (1. / 255)
IM_x, IM_y = IM.shape
	
for lost in xrange(changed_pixels):
	x_,y_ = random_integers(1,IM_x-2), random_integers(1,IM_y-2)
	val =  .1*randn() + .5
	IM[x_,y_] = max( min(val,1.), 0.)
imsave(name=("noised_"+imagename),arr=IM)
plt.imshow(IM, cmap=cm.gray)
plt.show()