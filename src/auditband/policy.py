import numpy as np

class ScaleUCB:
    """SC-UCB, with a deterministic prefix of trusted audits.

    Only audited truth may be supplied to update. A separate simulator has
    access to latent outcomes for evaluation. The empirical channel estimate
    uses signed agreement, which is unbiased under the shared symmetric model.
    """
    def __init__(self, costs, horizon, audit_budget, gamma0=.25, delta=None):
        self.costs=np.asarray(costs,dtype=float)
        self.costs=self.costs-self.costs.min()
        self.K=len(self.costs)
        if not 0 <= audit_budget <= horizon or not 0 < gamma0 <= 1:
            raise ValueError('Invalid budget or gamma0')
        self.horizon=int(horizon); self.budget=int(audit_budget); self.gamma0=gamma0
        self.delta=1/horizon**2 if delta is None else delta
        if not 0 < self.delta < 1: raise ValueError('delta must be in (0,1)')
        self.L=np.log(4*(self.K+1)*horizon/self.delta)
        self.counts=np.zeros(self.K,dtype=int); self.sums=np.zeros(self.K)
        self.agreement=0.; self.audits=0; self.t=0; self.pending=None

    @property
    def scale(self):
        return self.gamma0 if self.audits==0 else np.clip(self.agreement/self.audits,self.gamma0,1.)

    def choose(self):
        if self.pending is not None: raise RuntimeError('Previous action needs feedback')
        if self.t>=self.horizon: raise RuntimeError('Horizon exhausted')
        if self.t<self.K: arm=self.t
        else:
            idx=self.sums/self.counts+np.sqrt(self.L/(2*self.counts))-self.scale*self.costs
            arm=int(np.argmax(idx))
        audit=self.t<self.budget
        self.pending=(arm,audit)
        return arm,audit

    def update(self, proxy, truth=None):
        if self.pending is None: raise RuntimeError('Choose an action first')
        arm,audit=self.pending
        if proxy not in (0,1) or (audit and truth not in (0,1)) or (not audit and truth is not None):
            raise ValueError('Supply binary proxy and truth only on audited rounds')
        self.counts[arm]+=1; self.sums[arm]+=proxy
        if audit:
            self.agreement+=1. if proxy==truth else -1.
            self.audits+=1
        self.t+=1; self.pending=None


def default_budget(horizon, spread, audit_price):
    """Log-factor-free budget rule used in simulations (not constant optimal)."""
    if spread==0:return 0
    if audit_price==0:return horizon
    return min(horizon,int(np.ceil((spread*horizon/audit_price)**(2/3))))
