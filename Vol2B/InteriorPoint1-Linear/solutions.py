# solutions.py
"""Volume 2 Lab 19: Interior Point 1 (Linear Programs). Solution file."""

import numpy as np
from scipy import linalg as la
from scipy.stats import linregress
from matplotlib import pyplot as plt


# Auxiliary Functions =========================================================
def startingPoint(A, b, c):
    """Calculate an initial guess to the solution of the linear program
    min c^T x, Ax = b, x>=0.
    Reference: Nocedal and Wright, p. 410.
    """
    # Calculate x, lam, mu of minimal norm satisfying both
    # the primal and dual constraints.
    B = la.inv(A.dot(A.T))
    x = A.T.dot(B.dot(b))
    lam = B.dot(A.dot(c))
    mu = c - A.T.dot(lam)

    # Perturb x and s so they are nonnegative.
    dx = max((-3./2)*x.min(), 0)
    dmu = max((-3./2)*mu.min(), 0)
    x += dx*np.ones_like(x)
    mu += dmu*np.ones_like(mu)

    # Perturb x and mu so they are not too small and not too dissimilar.
    dx = .5*(x*mu).sum()/mu.sum()
    dmu = .5*(x*mu).sum()/x.sum()
    x += dx*np.ones_like(x)
    mu += dmu*np.ones_like(mu)

    return x, lam, mu

def randomLP(m,n):
    """Generate a linear program min c^T x s.t. Ax = b, x>=0.
    First generate m feasible constraints, then add
    slack variables to convert it into the above form.
    Inputs:
        m -- positive integer >= n, number of desired constraints
        n -- dimension of space in which to optimize
    Outputs:
        A -- array of shape (m,n+m)
        b -- array of shape (m,)
        c -- array of shape (n+m,), with m trailing 0s
        v -- the solution to the LP
    """
    # generate random constraints (each row corresponds to the normal
    # vector defining a linear constraint)
    A = np.random.random((m,n))*20 - 10

    # adjust so that the normal vector of each constraint lies in the upper
    # half-space. this ensures that the constraints permit a feasible region
    A[A[:,-1]<0] *= -1

    # adjust so that the solution to the program is a prescribed point v in
    # the first quadrant.
    v = np.random.random(n)*10
    #k = np.random.randint(n,m+1)
    k = n
    b = np.zeros(m)
    b[:k] = A[:k,:].dot(v)
    b[k:] = A[k:,:].dot(v) + np.random.random(m-k)*10

    # now create the appropriate c vector, a weighted sum of the first k
    # constraints
    c = np.zeros(n+m)
    c[:n] = A[:k,:].sum(axis=0)/k

    # at this point, we should have a program max c^T x s.t. Ax <= b, x >= 0
    # we need to convert it to standard equality form by adding slack variables
    A = np.hstack((A, np.eye(m)))

    # we now have the program min -c^T x s.t. Ax = b, x>=0.
    # the optimal solution has x[:n] = v
    return A, b, -c, v


# Problems 1-4 ================================================================
def interiorPoint(A, b, c, niter=20, tol=1e-16, verbose=False):
    """Solve the linear program min c^T x, Ax = b, x>=0
    using an Interior Point method.

    Parameters:
        A ((m,n) ndarray): Equality constraint matrix with full row rank.
        b ((m, ) ndarray): Equality constraint vector.
        c ((n, ) ndarray): Linear objective function coefficients.
        niter (int > 0): The maximum number of iterations to execute.
        tol (float > 0): The convergence tolerance.

    Returns:
        x ((n, ) ndarray): The optimal point.
        val (float): The minimum value of the objective function.
    """
    m,n = A.shape
    def F(x_, l_, m_):
        """The almost-linear function that accounts for the KKT conditions."""
        return np.hstack((np.dot(A.T, l_)+m_-c, np.dot(A, x_)-b, m_*x_))

    DF = np.zeros((2*n+m, 2*n+m))
    DF[:n,n:-n] = A.T
    DF[:n,-n:] = np.eye(n)
    DF[n:-n,:n] = A

    # Get the initial point and verify the dimensions.
    x, lam, mu = startingPoint(A, b, c)
    assert len(x) == len(mu) == len(c) == n
    assert len(lam) == len(b) == m

    e = np.ones_like(mu)
    sigma = .1

    i = 0
    nu = 1 + tol
    while i < niter and nu >= tol:
        i += 1

        # Problem 3: Search Direction
        DF[-n:,:n] = np.diag(mu)
        DF[-n:,-n:] = np.diag(x)

        nu = np.dot(x, mu) / n
        nu_vec = np.hstack((np.zeros(n+m), e*nu*sigma))
        lu_piv = la.lu_factor(DF)
        direct = la.lu_solve(lu_piv, nu_vec - F(x,lam,mu))

        # Problem 4: Step Length
        dx, dlam, dmu = direct[:n], direct[n:-n], direct[-n:]

        mask = dmu < 0
        amin = np.min(-mu[mask]/dmu[mask])
        alpha = min(1, .95*min(1, amin)) if np.any(mask) else .95

        mask = dx < 0
        dmin = np.min(-x[mask]/dx[mask]).min()
        delta = min(1, .95*min(1, dmin)) if np.any(mask) else .95

        # Problem 5: Finish it up.
        x += delta*dx
        lam += alpha*dlam
        mu += alpha*dmu

        if verbose:
            print("Iteration {:0>2} nu = {}".format(i, nu))
    if i < niter and verbose:
        print("Converged in {} iterations".format(i))
    elif verbose:
        print("Maximum iterations reached")
    return x, c.dot(x)

# Tests =======================================================================
def single_test(m=7, n=5, verbose=True):
    """Test interiorPoint() a single time."""
    A, b, c, x = randomLP(m, n)
    point, value = interiorPoint(A, b, c, verbose=verbose)
    if not np.allclose(x,point[:n]):
        return 1
    return 0

def single_other_test():
    m = np.random.randint(2,10)
    n = m
    A = np.random.random((m,n))*20 - 10
    A[A[:,-1]<0] *= -1
    x = np.random.random(n)*10
    b = A.dot(x)
    c = -A.sum(axis=0)/float(n)

    point, value = interiorPoint(A, b, c, verbose=True)
    if not np.allclose(x,point):
        return 1
    return 0


def huge_test(trials=100):
    """Test interior point in high dimensions 'trials' times."""
    from sys import stdout
    failed = 0
    for i in xrange(trials):
        print "\rIteration {} of {}".format(i+1, trials),
        stdout.flush()
        n = np.random.randint(low=100, high=200)
        m = np.random.randint(low=n, high=300)
        failed += test_interiorPoint(m, n, verbose=False)
        print "({} failures)".format(failed),
    print "{}/{} failed".format(failed, trials)


# Problem 5 ===================================================================
def leastAbsoluteDeviations(save=False):
    """This code should be fairly close to what the students submit for the
    least absolute deviations problem.
    """
    data = np.loadtxt('simdata.txt')
    m = data.shape[0]
    n = data.shape[1] - 1
    c = np.zeros(3*m + 2*(n + 1))
    c[:m] = 1
    y = np.empty(2*m)
    y[::2] = -data[:, 0]
    y[1::2] = data[:, 0]
    x = data[:, 1:]
    A = np.ones((2*m, 3*m + 2*(n + 1)))
    A[::2, :m] = np.eye(m)
    A[1::2, :m] = np.eye(m)
    A[::2, m:m+n] = -x
    A[1::2, m:m+n] = x
    A[::2, m+n:m+2*n] = x
    A[1::2, m+n:m+2*n] = -x
    A[::2, m+2*n] = -1
    A[1::2, m+2*n+1] = -1
    A[:, m+2*n+2:] = -np.eye(2*m, 2*m)

    sol = interiorPoint(A, y, c, niter=10, verbose=True)[0]
    beta = (sol[m:m+n] - sol[m+n:m+2*n])[0]
    b = sol[m+2*n] - sol[m+2*n+1]

    dom = np.linspace(0,10,2)
    plt.scatter(data[:,1], data[:,0], c='k')
    plt.plot(dom, beta*dom+b, 'b-', linewidth=2, label="LAD")

    # Compare with least squares
    slope, intercept = linregress(data[:,1], data[:,0])[:2]
    lstsq_line = slope*dom + intercept
    plt.plot(dom, lstsq_line, 'g--', linewidth=2, label="LSTSQ")

    # plt.title("Problem 5")
    plt.legend()
    if save is True: # For figure file creation
        plt.savefig("LADprob.pdf")
    else:
        plt.show()
    print 'Beta:', beta
    print 'b:', b


# =============================================================================
# Solutions using the old method (Predictor Corrector) ========================
# =============================================================================
def old_interiorPoint(A, b, c, niter=20, verbose=False, starting_point=None, pts=False):
    '''
    Solve the linear programming problem min c^T x, Ax = b, x>=0
    using an Interior Point method. This code is not optimized, but
    forms the basis for a common practical approach known as the
    Predictor-Corrector Algorithm.
    Inputs:
        A -- array of shape (m,n) with linearly independent rows
        b -- array of length m
        c -- array of length n
        niter -- positive integer giving the number of iterations
        starting_point -- tuple of arrays giving the initial values for x, l, and s.
                          if unspecified, the function startingPoint is used.
    Returns:
        x -- the optimal point
        val -- the minimum value of the objective function
        (pts -- list of points traced by the algorithm, returned if pts=True)
    Ref: Nocedal and Wright, p. 411
    '''
    pts = []
    # initialize variables
    m,n = A.shape
    if starting_point:
        x, l, s = starting_point
    else:
        x,l,s = startingPoint(A,b,c)
    pts.append(x)
    N = np.zeros((n+m+n, n+m+n))
    N[:n, n:n+m] = A.T
    N[:n, n+m:] = np.eye(n)
    N[n:n+m, :n] = A
    sol = np.empty(n+m+n)
    for k in xrange(niter):
        # finish initializing parts of the step equation
        N[n+m:, :n] = np.diag(s)
        N[n+m:, n+m:] = np.diag(x)
        r_c = (A.T).dot(l)+s-c
        r_b = A.dot(x)-b
        rhs = np.hstack((-r_c.ravel(), -r_b.ravel(), -x*s))

        # solve dx_aff, dl_aff, ds_aff using LU decomposition
        lu_piv = la.lu_factor(N)
        sol[:] = la.lu_solve(lu_piv, rhs)
        dx_aff = sol[:n]
        dl_aff = sol[n:n+m]
        ds_aff = sol[n+m:]

        # calculate a_p, a_d, mu_aff
        mask1 = dx_aff < 0
        if mask1.sum() > 0:
            a_p = min(1, ((-x/dx_aff)[mask1]).min())
        else:
            a_p = 1
        mask2 = ds_aff < 0
        if mask2.sum() > 0:
            a_d = min(1, (-s/ds_aff)[mask2].min())
        else:
            a_d = 1
        mu_aff = ((x+a_p*dx_aff)*(s+a_d*ds_aff)).sum()/np.float(n)

        # calculate mu times the centering parameter sig
        mu = (x*s).sum()/n
        musig = mu_aff**3/mu**2

        # calculate dx, dl, ds
        rhs[n+m:] += - dx_aff*ds_aff + musig
        sol[:] = la.lu_solve(lu_piv, rhs)
        dx = sol[:n]
        dl = sol[n:n+m]
        ds = sol[n+m:]

        # calculate ap, ad
        nu = 1-.1/(k+1)
        mask3 = dx < 0
        if mask3.sum() > 0:
            ap_max = (-x/dx)[mask3].min()
            ap = min(1, nu*ap_max)
        else:
            ap = 1
        mask4 = ds < 0
        if mask4.sum() > 0:
            ad_max = (-s/ds)[mask4].min()
            ad = min(1, nu*ad_max)
        else:
            ad = 1

        # step to new point
        x = x + ap*dx
        l = l + ad*dl
        s = s + ad*ds
        pts.append(x)

        if verbose:
            print '{0:f} {1:f}'.format((c*x).sum(), mu)

    if pts:
        return pts
    else:
        return x, (c*x).sum()

