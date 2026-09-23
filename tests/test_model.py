import numpy as np
import pytest
from fractions import Fraction as F
from auditband import paired_instance, joint_law, kl, compatible_interval, robust_winners, ScaleUCB

@pytest.mark.parametrize('D',[0,.001,.03,.125,.25])
@pytest.mark.parametrize('h',[1e-4,.005,.03,.125])
def test_paired_worlds(D,h):
    a,b=paired_instance(D,h,-1),paired_instance(D,h,1)
    np.testing.assert_allclose(a.proxy_means,b.proxy_means,atol=1e-14)
    for i in range(2):
        p,q=joint_law(a.means[i],a.gamma),joint_law(b.means[i],b.gamma)
        assert np.all(p>0) and np.all(q>0)
        assert kl(p,q)<=16*h*h+1e-14
        assert kl(q,p)<=16*h*h+1e-14
    if D:
        assert np.argmax(a.utilities)==1 and np.argmax(b.utilities)==0
        for e in (a,b):
            assert np.ptp(e.utilities)>=8*D*h/5-1e-14

def test_exact_rational_identity():
    for D in [F(1,4),F(1,8),F(1,100)]:
        for h in [F(1,8),F(1,16),F(1,256)]:
            for sign in [-1,1]:
                g=F(1,2)+sign*h
                mu=F(1,2)+D/(2*g)
                assert (1-g)/2+g*mu==F(1,2)+D/2
                assert mu-D-F(1,2)==-sign*D*h/g

def test_envelope():
    assert robust_winners([.5,.6],[0,.2],(.25,1))==[]
    assert robust_winners([.5,.6],[0,.2],(.25,.4))==[1]
    assert robust_winners([.5,.6],[0,.2],(.6,1))==[0]
    assert robust_winners([.5,.6],[0,.2],(.5,.5))==[0,1]
    assert compatible_interval([.95,.25])==(.8999999999999999,1.)

def test_certificate_independent_grid():
    rng=np.random.default_rng(712)
    for _ in range(200):
        v=rng.uniform(.1,.9,4); c=rng.uniform(0,.25,4); r=rng.uniform(0,.02,4)
        gs=np.linspace(.25,1,37)
        for i in robust_winners(v,c,(.25,1),r):
            for g in gs:
                for j in range(4):
                    if i!=j:assert v[i]-r[i]-g*c[i]>=v[j]+r[j]-g*c[j]-1e-12

def test_feedback_firewall_and_budget():
    p=ScaleUCB([0,.2],100,10)
    for t in range(100):
        i,a=p.choose()
        assert a==(t<10)
        if not a:
            with pytest.raises(ValueError):p.update(1,1)
        p.update(t%2,t%2 if a else None)
    assert p.audits==10 and p.scale==1
    with pytest.raises(RuntimeError):p.choose()

def test_signed_agreement_is_unbiased():
    for mu in np.linspace(0,1,19):
        for g in np.linspace(.25,1,17):
            p=joint_law(mu,g)
            assert abs(p@[1,-1,-1,1]-g)<1e-14
