import scipy as sp
from scipy import stats
import numpy as np
from numpy import random
import matplotlib as mpl
import seaborn as sns
sns.set()
# Exercise 1
T = 1000
a = sp.stats.norm.rvs(loc = 0, scale = 1, size = T)
b = sp.stats.norm.rvs(loc = 3, scale = 3, size = T)
c = sp.stats.uniform.rvs(loc = 0, scale = 1, size = T)
d = sp.stats.uniform.rvs(loc = -1, scale = 2, size = T)
e = sp.stats.gamma.rvs(1, scale = 2, size = T)
f = sp.stats.lognorm.rvs(s = 2, scale = np.exp(0.08), size = T)
#print(sp.stats.lognorm.fit(f))

# Exercises 2
print(sp.stats.kstest(a, sp.stats.norm(loc = 0, scale = 1).cdf))
print(sp.stats.kstest(b, 'norm', (3,3)))
print(sp.stats.kstest(c, 'uniform', (0,1)))
print(sp.stats.kstest(d, 'uniform', (-1,2)))
#print(sp.stats.kstest(d, sp.stats.uniform(-1,2).cdf))
print(sp.stats.kstest(e, 'gamma', (1,0,2)))
#print(sp.stats.kstest(e, sp.stats.gamma(1, scale = 2).cdf))
print(sp.stats.kstest(f, 'lognorm', (2, 0,np.exp(0.08))))
#print(sp.stats.kstest(f, sp.stats.lognorm(s = 2, scale = np.exp(0.08)).cdf))

# Exercise 3
np.random.seed()

# Exercise 4
st = np.random.get_state()
print(sp.stats.norm.rvs(loc = 0, scale = 1, size = 10))
np.random.set_state(st)
print(sp.stats.norm.rvs(loc = 0, scale = 1, size = 10))

# Exercise 5
def descriptive_stats(data):
    mean = np.mean(data)
    std = np.std(data)
    skew = sp.stats.skew(data)
    kurtosis = sp.stats.kurtosis(data, fisher = False)
    return mean, std, skew, kurtosis

print(descriptive_stats(a))

# Exercise 6
cov = np.array([[1, -0.5],[-0.5, 1]])
print(cov)
bivariate_norm = sp.stats.multivariate_normal.rvs(cov = cov, size = 100)
print(bivariate_norm)

print(sp.stats.pearsonr(bivariate_norm[:,0], bivariate_norm[:,1]))
print(sp.stats.spearmanr(bivariate_norm[:,0], bivariate_norm[:,1]))
print(sp.stats.kendalltau(bivariate_norm[:,0], bivariate_norm[:,1]))

# Exercise 7
gamma = sp.stats.gamma(1, scale = 2)
print(gamma.median())
gamma_sample = gamma.rvs(size = 10000)
print(np.median(gamma_sample))
fig1 = mpl.pyplot.figure()
mpl.pyplot.hist(gamma_sample, bins = 50)
mpl.pyplot.autoscale(tight='x')
mpl.pyplot.tight_layout()
fig1.savefig('Chapter19_Ex7_Hist.pdf')

# Exercise 8
fig2 = mpl.pyplot.figure()
ax_a = fig2.add_subplot(321)
res_a = sp.stats.probplot(a, dist=sp.stats.norm, sparams=(0,1), plot = ax_a)
ax_b = fig2.add_subplot(322)
res_b = sp.stats.probplot(b, dist=sp.stats.norm, sparams=(3,3), plot = ax_b)
ax_c = fig2.add_subplot(323)
res_c = sp.stats.probplot(c, dist=sp.stats.uniform, sparams=(0,1), plot = ax_c)
ax_d = fig2.add_subplot(324)
res_d = sp.stats.probplot(d, dist=sp.stats.uniform, sparams=(-1,2), plot = ax_d)
ax_e = fig2.add_subplot(325)
res_e = sp.stats.probplot(e, dist=sp.stats.gamma, sparams=(1,0,2), plot = ax_e)
ax_f = fig2.add_subplot(326)
res_f = sp.stats.probplot(f, dist=sp.stats.lognorm, sparams=(2, 0, np.exp(0.08)), plot = ax_f)
mpl.pyplot.autoscale(tight='x')
mpl.pyplot.tight_layout()
fig2.savefig('Chapter19_Ex8_Probplots.pdf')
