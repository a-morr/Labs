import matplotlib
# matplotlib.rcParams = matplotlib.rc_params_from_file('../../matplotlibrc')
import numpy as np
from matplotlib import pyplot as plt
import scipy.optimize as opt

# Load in the data
data = np.load("convection.npy")
initial = 4

# Define the function to optimize.
def nu(R, c, beta):
    return c*R**beta

# Use curve_fit and the data to get the parameters.
popt, pcov = opt.curve_fit(nu, data[initial:,0], data[initial:,1])
curve = nu(data[initial:,0], popt[0], popt[1])

# Plot the data and the curve.
plt.loglog(data[:,0], data[:,1], '.k', label='Data')
plt.loglog(data[initial:,0], curve, 'b', label='Curve', linewidth=2)
plt.legend(loc="lower right")
# plt.show()

# Save the plot.
plt.savefig("ConvectionFit.pdf")