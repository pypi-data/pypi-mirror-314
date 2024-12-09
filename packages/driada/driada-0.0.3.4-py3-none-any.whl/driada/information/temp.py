import numpy as np

from .info_base import *
from .ksg import *

def gaussian_entropy_theory(sigma):
    if sigma.shape[0] != sigma.shape[1]:
        raise ValueError('Covariance matrix should be square!')
    sigma_det = np.linalg.det(sigma)
    k = sigma.shape[0]
    theory_entropy = 0.5/np.log(2)*np.log((2*np.pi*np.e)**k*sigma_det)
    return theory_entropy


def gaussian_mi_theory(sigma1, sigma2, sigma12):
    if isinstance(sigma1, float):
        sigma_det1 = sigma1
    else:
        sigma_det1 = np.linalg.det(sigma1)

    if isinstance(sigma1, float):
        sigma_det2 = sigma2
    else:
        sigma_det2 = np.linalg.det(sigma2)

    sigma_det12 = np.linalg.det(sigma12)
    theory_mi = 0.5/np.log(2)*np.log(sigma_det1*sigma_det2/sigma_det12)
    return theory_mi


#data = np.random.choice([0,1], size=1000, p=[0.1, 0.9])
p=-0.9
C = np.array([[1, p], [p, 1]])
n=2
T=10000
data = np.random.multivariate_normal(np.zeros(n),
                                    C,
                                    size=T,
                                    check_valid='raise').T*100
#print(data)
ds = 1
ts1 = TimeSeries(data[0,:])
ts2 = TimeSeries(data[1,:])
discrete_data = np.random.choice([0,1], size=T, p=[0.1, 0.9])
ts3 = TimeSeries(discrete_data)

entr = {}

'''
if ts.discrete:
    counts = []
    for val in np.unique(ts.data[::ds]):
        counts.append(len(np.where(ts.data[::ds] == val)[0]))

    print('discrete')
    entr[ds] = entropy(counts, base=np.e)

else:
    print('continuous')
    entr1 = get_tdmi(ts.scdata[::ds], min_shift=1, max_shift=2)[0]
    entr2 = nonparam_entropy_c(ts.data, k=5)/np.log(2)
'''

k=10

mi1 = get_1d_mi(ts1, ts2, estimator='gcmi')
mi2 = nonparam_mi_cc_mod(ts1.data, ts2.data, k=k,
                        precomputed_tree_x=ts1.get_kdtree(),
                        precomputed_tree_y=ts2.get_kdtree())/np.log(2)

H1 = nonparam_entropy_c(ts1.data, k=k)/np.log(2)
H2 = nonparam_entropy_c(ts2.data, k=k)/np.log(2)
H12 = nonparam_entropy_c(np.c_[ts1.data, ts2.data], k=k)/np.log(2)
mi3 = H1 + H2 - H12
print(H12, H1, H2)

#print('theory:', gaussian_entropy_theory(C))
print('theoretic MI:', gaussian_mi_theory(C[0,0], C[1,1], C))
print('gcmi:', mi1)
print('ksg:', mi2)
print('entropy-based:', mi3)
print('entropy:', H2)