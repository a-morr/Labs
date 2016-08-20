import numpy as np
import scipy.sparse as spar
import scipy.linalg as la
from scipy.sparse import linalg as sla

def to_matrix(filename,n):
    '''
    Return the nxn adjacency matrix described by datafile.
    INPUTS:
    datafile (.txt file): A .txt file describing a directed graph. Lines
        describing edges should have the form '<from node>\t<to node>\n'.
        The file may also include comments.
    n (int): The number of nodes in the graph described by datafile
    RETURN:
        Return a SciPy sparse `dok_matrix'.
    '''
    adj = spar.dok_matrix((n,n))
    with open(filename, 'r') as myfile:
        for line in myfile:
            line = line.strip().split()
            try:
                x,y = int(line[0]),int(line[1])
                adj[x,y] = 1
            except:
                continue
    return adj

def calculateK(A,N):
    '''
    Compute the matrix K as described in the lab.
    Input:
        A (array): adjacency matrix of an array
        N (int): the datasize of the array
    Return:
        K (array)
    '''
    n = A.shape[0]
    D = np.zeros(n)
    for row in range(n):
        D[row] = A[row].sum()
    for i in range(n):
        if D[i] == 0:
            D[i] = n
            A[i] = np.ones(n)
    K = (A.T/D)
    return K[:N,:N]

def iter_solve(adj, N=None, d=.85, tol=1E-5):
    '''
    Return the page ranks of the network described by `adj`.
    Iterate through the PageRank algorithm until the error is less than `tol'.
    Inputs:
    adj - A NumPy array representing the adjacency matrix of a directed graph
    N (int) - Restrict the computation to the first `N` nodes of the graph.
            Defaults to N=None; in this case, the entire matrix is used.
    d     - The damping factor, a float between 0 and 1.
            Defaults to .85.
    tol  - Stop iterating when the change in approximations to the solution is
        less than `tol'. Defaults to 1E-5.
    Returns:
    The approximation to the steady state.
    '''
    if N is None:
        N = adj.shape[1]
    pt = np.ones((N,1))/N    
    K = calculateK(adj,N)
    pt1 = d*np.dot(K,pt) + ((1.-d)/N)*np.ones((N,1))
    while la.norm(pt1-pt) > tol:
        pt = pt1
        pt1 = d*np.dot(K,pt) + ((1.-d)/N)*np.ones((N,1))
    return pt1

def eig_solve( adj, N=None, d=.85):
    '''
    Return the page ranks of the network described by `adj`. Use the
    eigenvalue solver in \li{scipy.linalg} to calculate the steady state
    of the PageRank algorithm
    Inputs:
    adj - A NumPy array representing the adjacency matrix of a directed graph
    N - Restrict the computation to the first `N` nodes of the graph.
            Defaults to N=None; in this case, the entire matrix is used.
    d     - The damping factor, a float between 0 and 1.
            Defaults to .85.
    Returns:
    The approximation to the steady state.
    '''
    if N is None:
        N = adj.shape[1]
    K = calculateK(adj,N)
    B = d*K + ((1.-d)/N)*np.ones((N,N))
    evalues,evectors = la.eig(B)
    i = np.argsort(evalues)[-1] #Find index of largest eigenvalue (which should be 1)
    pt = (evectors[:,i].real)
    pt = pt*1/pt.sum()
    return pt
    
def team_rank(filename='ncaa2013.csv'):
    '''
    Use your iterative PageRank solver to predict the rankings of the teams in
    the given dataset of games.
    The dataset should have two columns, representing winning and losing teams.
    Each row represents a game, with the winner on the left, loser on the right.
    Parse this data to create the adjacency matrix, and feed this into the
    solver to predict the team ranks.
    Inputs:
    filename (optional) - The name of the dataset.
    Returns:
    ranks - A list of the ranks of the teams in order "best" to "worst"
    teams - A list of the names of the teams, also in order "best" to "worst"
    '''
    # Create adj. matrix
    teams = set()
    wins = []
    with open(filename, 'r') as f:
        f.readline() #read the header
        for line in f:
            data = line.strip().split(',') #split on commas
            teams.add(data[0])
            teams.add(data[1])
            wins.append(data)
    n = len(teams)
    team_list = list(teams)
    team_number = dict()
    for i, t in enumerate(team_list):
        team_number[t] = i
    adj = spar.dok_matrix((n,n)) #adjacency matrix
    for match in wins:
        win_number = team_number[match[0]]
        lose_number = team_number[match[1]]
        adj[lose_number,win_number] = 1
    
    # Solve for ranks
    p = iter_solve(adj.todense(), d=0.7)
    p = np.array(p).squeeze()
    idx = np.argsort(p)[::-1]
    n_out = 5
    return [p[j] for j in idx[:n_out]], [team_list[j] for j in idx[:n_out]]
    
def problemOne():
    print to_matrix('datafile.txt',8).todense()

def problemTwo():
    A = to_matrix('datafile.txt',8).todense()
    print calculateK(A,8)

def problemThree():
    A = to_matrix('datafile.txt',8).todense()
    print iter_solve(A,N = 8)

def problemFour():
    A = to_matrix('datafile.txt',8).todense()
    a =iter_solve(A,N = 8)
    b = eig_solve(A,N = 8)
    print a
    print eig_solve(A,N=8)

if __name__ == '__main__':
    print "Testing 1"
    problemOne()
    print "Testing 2"
    problemTwo()
    print "Testing 3"
    problemThree()
    print "Testing 4"
    problemFour()
    print "Testing team rank"
    ranks, teams = team_rank()
    print ranks
    print teams