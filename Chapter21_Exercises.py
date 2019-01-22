import scipy as sp
import scipy.optimize as opt
import numpy as np
from numpy import random, linalg
from scipy import stats
# Exercise 1
def MLE_mu(mu, x):
    theta = [mu, 1]
    return sp.stats.norm.nnlf(theta,x)

x = np.random.randn(1000)
mu0 = 0
mu_hat_bfgs = opt.fmin_bfgs(MLE_mu, mu0, args = (x,))
print(mu_hat_bfgs)
mu_hat = opt.fmin(MLE_mu, mu0, args= (x,))
print(mu_hat)
print(np.mean(x))

# Exercise 2
sigma_sq0 = 1
theta0 = [mu0, sigma_sq0]
def MLE(theta, x, printX = False):
    theta_test = theta
    #print(theta)
    theta_test[1] = np.sqrt(theta[1])
    #if printX:
     #   print(theta)
    #print(theta_test)
    return sp.stats.norm.nnlf(theta_test, x)
theta_hat = opt.fmin_slsqp(MLE, theta0, args = (x,), bounds = [(-1000, 1000), (0.00001, 1000000)])
#MLE(theta_hat, x, printX = True)
print(theta_hat)
# Exercise 3
sigma0 = np.sqrt(sigma_sq0)
theta0 = [mu0, sigma0]
def MLE(theta, x):
    return sp.stats.norm.nnlf(theta, x)
def std_constraint(theta, x):
    return np.array(theta[1])
theta_hat = opt.fmin_slsqp(MLE, theta0, f_ieqcons = std_constraint, args = (x,))
print(theta_hat)

# Exercise 4
T = 1000
K = 4
X = np.random.randn(T,K)
y = 100*np.random.randn(T) + 6
print(y)
args = (y, X)
beta_OLS = np.linalg.inv(X.T @ X) @ (X.T @ y)
print(beta_OLS)
def MLE_beta(beta, y, X):
    e = y - X @ beta.T
    return sp.stats.norm.nnlf([0, 1], e)
beta_hat = opt.fmin_bfgs(MLE_beta, beta_OLS + 3, args = args)
print(beta_hat)
