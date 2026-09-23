import numpy as np
from auditband.model import ambiguity_lp,compatible_interval

def test_lp_against_grid_and_two_arm_closed_form():
    for D in [.02,.1,.2,.25]:
        v=np.array([.5,.5+D/2]);c=np.array([0,D])
        p,value=ambiguity_lp(v,c)
        lo,hi=compatible_interval(v)
        bminus=D/(2*lo)-D;bplus=D-D/(2*hi)
        expected=bminus*bplus/(bminus+bplus)
        assert abs(value-expected)<1e-12
        grid=[]
        for g in np.linspace(lo,hi,251):
            u=.5+(v-.5)/g-c;grid.append(max(u)-p@u)
        assert abs(max(grid)-value)<1e-12

def test_k_arm_lp_endpoint_reduction():
    rng=np.random.default_rng(411)
    for _ in range(80):
        K=int(rng.integers(2,15));v=rng.uniform(.05,.95,K);c=rng.uniform(0,.4,K)
        p,val=ambiguity_lp(v,c);lo,hi=compatible_interval(v)
        assert abs(sum(p)-1)<1e-9 and min(p)>-1e-9
        for g in np.linspace(lo,hi,113):
            u=.5+(v-.5)/g-c
            assert max(u)-p@u<=val+1e-9

def test_zero_spread_needs_no_calibration():
    for v in ([.4,.6],[.6,.6],[.1,.7,.4]):
        p,val=ambiguity_lp(v,np.zeros(len(v)))
        assert abs(val)<1e-12
        assert p@np.array(v)>=max(v)-1e-12
