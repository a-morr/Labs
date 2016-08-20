# solutions.py
"""Volume II: Compressed Sensing. Solutions file."""


import numpy as np
from cvxopt import matrix, solvers
from matplotlib import pyplot as plt
from visualize2 import visualizeEarth
from camera import Camera


# Problem 1
def l1Min(A, b):
    """Calculate the solution to the optimization problem

        minimize    ||x||_1
        subject to  Ax = b

    Return only the solution x (not any slack variable), as a flat NumPy array.

    Parameters:
        A ((m,n) ndarray)
        b ((m, ) ndarray)

    Returns:
        x ((n, ) ndarray): The solution to the minimization problem.
    """

    assert A.shape[0] == b.shape[0], "mismatched dimensions"

    n = A.shape[1]
    I = np.eye(n, dtype=np.float)

    '''The optimization problem to solve (via cvxopt) is:

    minimize                [u]
                      [1 0] [x]

    subject to      [-I  I] [u]     [0]
                    [-I -I] [x]  <= [0]

                            [u]
                    [0   A] [x]  ==  b
    '''

    # Build the matrices for cvxopt (make sure dtype=np.floats)
    c = matrix(np.hstack((np.ones(n), np.zeros(n))).astype(np.float))
    G = matrix(np.vstack((np.hstack((-I, I)),np.hstack((-I, -I)))))
    h = matrix(np.zeros(2*n))
    new_A = matrix(np.hstack((np.zeros_like(A), A)).astype(np.float))
    new_b = matrix(b.astype(np.float))

    # Perform the optimization.
    sol = solvers.lp(c, G, h, new_A, new_b)

    # Flatten out the array and only get the x value.
    return np.array(sol['x']).ravel()[n:]


# Problem 2
def prob2(filename='ACME.png'):
    """Reconstruct the image in the indicated file using 100, 200, 250,
    and 275 measurements. Seed NumPy's random number generator with
    np.random.seed(1337) before each measurement to obtain consistent
    results.

    Resize and plot each reconstruction in a single figure with several
    subplots (use plt.imshow() instead of plt.plot()). Return a list
    containing the Euclidean distance between each reconstruction and the
    original image.
    """
    image = 1 - plt.imread(filename)[:,:,0]
    measurements, err = [100, 200, 250, 275], []
    
    for m in measurements:
        # Get 'm' random measurements.
        np.random.seed(1337)
        A = np.random.randint(0, 2, (m, image.shape[0]*image.shape[1]))
        b = A.dot(image.flatten())

        # Reconstruct the image and calculate the 2-norm error.
        reconstruction = l1Min(A, b).reshape(image.shape)
        err.append(np.linalg.norm(image - reconstruction))

        # Plot the image.
        plt.subplot(2, 2, measurements.index(m)+1)
        plt.imshow(reconstruction)
        plt.title("{} measurements".format(m))

    # Show the subplots and return the error list.
    plt.suptitle("Reconstruction of {}".format(filename))
    plt.show()
    
    return err

# Problem 3
def prob3(filename="StudentEarthData.npz", show=True):
    """Reconstruct single-pixel camera color data in StudentEarthData.npz
    using 450, 650, and 850 measurements. Seed NumPy's random number generator
    with np.random.seed(1337) before each measurement to obtain consistent
    results.

    Return a list containing the Euclidean distance between each
    reconstruction and the color array.
    """

    # Load the data.
    data = np.load(filename)
    faces, vertices = data['faces'], data['vertices']
    colors, V = data['C'], data['V']
    measurements, err = [250, 400, 550], []

    for m in measurements:
        # Get 'm' random measurements.
        np.random.seed(1337)
        results = []

        camera = Camera(faces, vertices, colors)
        camera.add_lots_pic(m)
        A, B = camera.returnData()

        # Do compressed sensing on each channel.
        for b in B.T:
            reconstruction = l1Min(A.dot(V), b)
            results.append(V.dot(reconstruction))
    
        # Reconstruct the results, calculate the error, and show the globe.
        results = np.column_stack(results)
        err.append(np.linalg.norm(colors - results, ord=np.inf))
        if show is True:
            visualizeEarth(faces, vertices, results.clip(0,1))

    if show is True:
        # True image.
        visualizeEarth(faces, vertices, colors)

    return err

if __name__ == '__main__':
    pass
    # prob2_err()
    print prob3(show=True)