import importlib.util
from pathlib import Path
import numpy as np
import pytest
from auditband import ScaleUCB
spec=importlib.util.spec_from_file_location('runs',Path(__file__).parents[1]/'scripts/run_experiments.py')
runs=importlib.util.module_from_spec(spec);spec.loader.exec_module(runs)

@pytest.mark.parametrize('B',[0,1,37,299,300])
def test_reference_implementation_matches_fast_simulator(B):
    T,seed=300,91
    mu=np.array([.5,.75]);c=np.array([0,.2]);g=.4
    p=ScaleUCB(c,T,B)
    np.random.seed(seed); regret=0.
    for t in range(T):
        i,a=p.choose();y=int(np.random.random()<mu[i]);u=np.random.random()
        z=int(u>=(1-g)/2) if y else int(u<(1-g)/2)
        p.update(z,y if a else None);regret+=max(mu-c)-(mu[i]-c[i])
    trace,ghat=runs.simulate(mu,c,np.full(2,.3),np.full(2,.3),T,B,.2,seed,0)
    np.testing.assert_allclose(trace[-1],[regret,B,regret+.2*B],rtol=0,atol=1e-12)
    assert abs(p.scale-ghat)<1e-12
