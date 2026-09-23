from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Environment:
    means: np.ndarray
    costs: np.ndarray
    gamma: float
    audit_price: float = 0.2

    def __post_init__(self):
        means, costs = np.asarray(self.means, dtype=float), np.asarray(self.costs, dtype=float)
        if means.ndim != 1 or means.shape != costs.shape or len(means) < 2:
            raise ValueError('Matching one-dimensional arrays of at least two arms required')
        if np.any((means < 0) | (means > 1)) or np.any(costs < 0):
            raise ValueError('Means must be probabilities; costs must be nonnegative')
        if not 0 < self.gamma <= 1 or self.audit_price < 0:
            raise ValueError('Invalid channel or audit price')
        object.__setattr__(self, 'means', means)
        object.__setattr__(self, 'costs', costs)

    @property
    def proxy_means(self):
        return (1-self.gamma)/2 + self.gamma*self.means

    @property
    def utilities(self):
        return self.means-self.costs


def paired_instance(spread, h, sign, audit_price=0.2):
    if not 0 <= spread <= .25 or not 0 < h <= .125 or sign not in (-1, 1):
        raise ValueError('Require D in [0,1/4], h in (0,1/8], sign +/-1')
    gamma = .5 + sign*h
    return Environment(np.array([.5, .5+spread/(2*gamma)]), np.array([0.,spread]), gamma, audit_price)


def joint_law(mu, gamma):
    """Probabilities ordered as (Y,Z)=(0,0),(0,1),(1,0),(1,1)."""
    q = (1+gamma)/2
    return np.array([(1-mu)*q, (1-mu)*(1-q), mu*(1-q), mu*q])


def kl(p, q):
    p, q = np.asarray(p), np.asarray(q)
    if np.any((p > 0) & (q == 0)):
        return np.inf
    mask = p > 0
    return float(np.sum(p[mask] * np.log(p[mask]/q[mask])))


def compatible_interval(proxy_means, gamma0=.25):
    v = np.asarray(proxy_means)
    if np.any((v < 0) | (v > 1)) or not 0 < gamma0 <= 1:
        raise ValueError('Invalid proxy probabilities or lower reliability bound')
    return max(gamma0, float(np.max(np.abs(2*v-1)))), 1.


def robust_winners(proxy_means, costs, interval, radii=None):
    """Actions certified best for all proxy means in the box and all slopes.

    A returned i satisfies hat_lambda_i-r_i-g*c_i >=
    hat_lambda_j+r_j-g*c_j for every j != i at both interval endpoints.
    Without radii this is the exact common-maximizer set for known proxy means.
    """
    v, c = np.asarray(proxy_means), np.asarray(costs)
    r = np.zeros_like(v) if radii is None else np.asarray(radii)
    lo, hi = interval
    if len(v) != len(c) or r.shape != v.shape or lo > hi or np.any(r < 0):
        raise ValueError('Invalid confidence region')
    out=[]
    for i in range(len(v)):
        certified=True
        for j in range(len(v)):
            if i == j: continue
            for g in (lo,hi):
                if v[i]-r[i]-v[j]-r[j]-g*(c[i]-c[j]) < -1e-12:
                    certified=False
        if certified: out.append(i)
    return out


def ambiguity_lp(proxy_means, costs, gamma0=.25):
    """Exact no-audit minimax mixture when proxy means are supplied.

    Solves a small linear program with 2K constraints. Numerical optimizer
    output is not an interval-arithmetic proof certificate.
    """
    from scipy.optimize import linprog
    v,c=np.asarray(proxy_means),np.asarray(costs)
    low,high=compatible_interval(v,gamma0)
    if c.shape!=v.shape:raise ValueError('Matching costs required')
    K=len(v);A=[];b=[]
    for g in (low,high):
        u=.5+(v-.5)/g-c
        for i in range(K):
            A.append(np.r_[-u,-1.]);b.append(-u[i])
    result=linprog(np.r_[np.zeros(K),1.],A_ub=A,b_ub=b,
                  A_eq=[np.r_[np.ones(K),0.]],b_eq=[1.],bounds=[(0,1)]*K+[(0,None)],method='highs')
    if not result.success:raise RuntimeError(result.message)
    return result.x[:-1],max(0.,result.fun)
