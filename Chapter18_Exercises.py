import numpy as np
from numpy import linalg, random
import pandas as pd

# Exercise 1
def as_category(A):
    r""" Transform T*1 array of categorical variables into an array of binaries, with columns mathing the sorted list of unique values in the original array. Return 1) the indicators array 2) the list of categories (also in form of an array)

    Parameter
    ---------
    A : ndarray
    The original values

    Returns
    -------
    indicators : ndarray
    The resulting set of binary indicator variables : rows match the values of A and columns, the categorical values

    categories : ndarray
    The array of categories

    Examples
    --------

    >>> A = np.array([1,4,1,5,2,2,2])

    >>> indicators, categories = as_category(A)
    
    """
    T = A.shape[0]
    categories = np.unique(A)
    C = categories.shape[0]
    indicators = np.zeros((T, C))
    for i in range(T):
        for c in range(C):
            indicators[i, c] = (A[i] == categories[c])
    return indicators, categories

# Checking input :
# print(A)
# Checking outputs :
# print(indicators)
# print(categories)
# print(type(indicators))
# print(type(categories))

# Exercise 2
def gls(X, y, Omega = None):
    T = X.shape[0]
    if np.logical_or(y.shape[0] != T, y.ndim != 1):
        return 0
    K = X.shape[1]
    if Omega is None:
        Omega = np.eye(T)
    beta = np.linalg.inv(X.T @ np.linalg.inv(Omega) @ X) @ X.T @ np.linalg.inv(Omega) @ y
    return beta

X = np.random.randn(1000,3)
X_withconst = np.hstack((np.ones((X.shape[0],1)),X))
y = np.random.randn(1000)
#print(X)
#print(y)
beta_GLS = gls(X, y)
print(beta_GLS)
# Checking with the standard OLS function
m = np.linalg.lstsq(X,y, rcond = None)[0]
print(m)

# Exercise 3
def partial_corr(x, y = None, quantile = 0.5, tail = 'Lower'):
    if y is not None:
        X = x
        Y = y
        T = X.shape[0]
        X.shape = T,1
        Y.shape = T,1
        Z = np.hstack((X,Y))
    else:
        Z = x
    T, K = Z.shape
    indicator = np.zeros((T, K))
    part_corr_coef = np.zeros((K, K))
    nvalues = np.zeros((K, K))
    for i, z in enumerate(Z.T):
        cutoff = np.quantile(z, quantile)
        #print(z <= quantile)
        indicator[:,i] = (z <= cutoff)
    print(indicator)
    if tail == 'Upper':
        indicator = 1 - indicator
    for i in range(K):
        for j in range(K):
            selector = np.logical_and(indicator[:,i], indicator[:,j])
            selected_Z = Z[:, np.r_[i,j]]
            selected_Z = selected_Z[selector]
            nvalues[i, j] = np.sum(selector)
            if nvalues[i, j] > 1:
                #print(selected_Z)
                part_corr_coef[i, j] = np.corrcoef(selected_Z.T)[0,1]
            else:
                part_corr_coef[i, j] = np.nan
            #print(nvalues)
    return part_corr_coef, nvalues

x = np.random.randn(100)
y = np.random.randn(100)
#print(x)
#print(y)
part_corr_coef, nvalues = partial_corr(x,y, quantile = 0)
print(part_corr_coef)
print(nvalues)
print(np.corrcoef(x,y, rowvar=False))




