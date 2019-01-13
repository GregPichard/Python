import numpy as np

# Exercise 1
r1 = np.random.randn(1)
r2 = np.random.randn(1)
print(r1)
print(r2)
if (r1 >= 0) & (r2 >= 0):
    print('Both positive')
elif (r1 < 0) & (r2 < 0):
    print('Both negative')
else:
    print('Mixed signs')

# Exercise 2 - ARMA(2,2)
T = 1000
y = np.zeros(2*T)
e = np.random.randn(2*T)
phi1 = 1.4
phi2 = -0.8
theta1 = 0.4
theta2 = 0.8

for i in range(2, 2*T):
    y[i] = phi1*y[i-1] + phi2*y[i-2] + theta1*e[i-1] + theta2*e[i-2] + e[i]
y = y[T:]

# Exercise 3 - GARCH(1,1)
omega = 0.05
alpha = 0.05
beta = 0.9
y = np.zeros(2*T)
sigma2 = np.zeros(2*T)
e = np.random.randn(2*T)
for i in range(1, 2*T):
    sigma2[i] = omega + alpha * y[i - 1]**2 + beta * sigma2[i - 1]
    y[i] = np.sqrt(sigma2[i]) * e[i]
y = y[T:]
sigma2 = sigma2[T:]

# Exercise 4 - GJR-GARCH(1,1,1)
omega = 0.05
alpha = 0.02
gamma = 0.07
beta = 0.9
y = np.zeros(2*T)
sigma2 = np.zeros(2*T)
e = np.random.randn(2*T)
for i in range(1, 2*T):
    sigma2[i] = omega + alpha * y[i - 1]**2 + gamma * (y[i - 1] < 0) * y[i - 1]**2 + beta * sigma2[i - 1]
    y[i] = np.sqrt(sigma2[i]) * e[i]
y = y[T:]
sigma2 = sigma2[T:]

# Exercise 5 - ARMA(1,1) - GJR-GARCH(1,1) - in mean
phi1 = -0.1
theta1 = 0.4
p_lambda = 0.03
y = np.zeros(2*T)
sigma2 = np.zeros(2*T)
e = np.random.randn(2*T)
for i in range(1, 2*T):
    sigma2[i] = omega + alpha * sigma2[i - 1] * e[i - 1]**2 + gamma * (e[i - 1] < 0) * sigma2[i - 1] * e[i - 1]**2 + beta * sigma2[i - 1]
    y[i] = phi1 * y[i - 1] + theta1 * np.sqrt(sigma2[i - 1]) * e[i - 1] + p_lambda * sigma2[i] + np.sqrt(sigma2[i]) * e[i]
y = y[T:]
sigma2 = sigma2[T:]

# Exercise 6
# 1
D = 5
A = np.zeros((D,D))
for i in range(D):
    for j in range(D):
        A[i, j] = i * j
print(A)

#2
B = np.zeros((D,D))
for i, r in enumerate(B):
    for j, c in enumerate(r):
        B[i, j] = i * j
print(B)

# Exercise 7
import scipy as sp
from scipy import stats
def BisecSearchNormCDF(p):
    u_bound = 6
    l_bound = -u_bound
    d = 2 * u_bound
    while (d > 1e-9):
        midpoint = 0.5*(u_bound + l_bound)
        if p >= sp.stats.norm.cdf(midpoint):
            l_bound = midpoint
        else:
            u_bound = midpoint
        d = abs(u_bound - l_bound)
    return midpoint

# Exercise 8
l = list([0.01,0.5,0.975])
for p in l:
    a = BisecSearchNormCDF(p)
    b = sp.stats.norm.ppf(p)
    print(a)
    print(b)
    print(abs(a - b))
# Exercise 9
x = np.random.randn(10)
y = [v for v in x if v < 0]
print(x)
print(y)
