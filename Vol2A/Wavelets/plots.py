# plots.py
import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file('../../matplotlibrc')

import numpy as np
from matplotlib import pyplot as plt
from scipy import misc

def grey_image(filename, greyname):
    "Create a grayscale version of a color image"
    image = misc.imread(filename,True)
    plt.imsave("figures/"+greyname, image, cmap='gray')

def noise_image(filename, noisename):
    "Create a noised version of a grayscale image"
    image = misc.imread(filename,True)
    noiseSigma = 16.0
    image += np.random.normal(0, noiseSigma, size=image.shape)
    plt.imsave("figures/"+noisename, image, cmap='gray')

grey_image("swanlake.jpg", "swanlake_gray.jpg")
noise_image("swanlake_gray.jpg", "swanlake_polluted.jpg")
