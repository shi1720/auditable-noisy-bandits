#!/usr/bin/env python3
"""Frozen synthetic study. All outcomes generated here; no API/model claims."""
from pathlib import Path
import sys, csv, json, hashlib, time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
from numba import njit
from auditband.policy import default_budget
ROOT=Path(__file__).resolve().parents[1]
METHODS=['SC-UCB','Oracle-scale UCB','Naive proxy UCB','Rank-only UCB','Audit-only ETC','Audit-all UCB']

@njit(cache=False)
def simulate(mu,c,fp,fn,T,B,a,seed,method):
    # Fixed random stream per seed shared by methods. Each round uses two draws,
    # irrespective of the selected action or whether the outcome is audited.
    np.random.seed(seed)
    K=len(mu); n=np.zeros(K); s=np.zeros(K); yn=np.zeros(K); ys=np.zeros(K)
    agree=0.; audits=0; regret=0.; chosen=0; L=np.log(4*(K+1)*T**3)
    checkpoints=np.array([T//4,T//2,T],dtype=np.int64)
    trace=np.zeros((3,3)); cp=0
    best=np.max(mu-c)
    for t in range(T):
        g=.25 if audits==0 else min(1.,max(.25,agree/audits))
        if method==1: g=1-fp[0]-fn[0]
        elif method==2: g=1.
        elif method==3:g=0.
        if method==4:
            if t<B: chosen=t%K
            else:
                chosen=0; top=-1e100
                for i in range(K):
                    v=(ys[i]/yn[i] if yn[i]>0 else .5)-c[i]
                    if v>top:chosen=i;top=v
        elif method==5:
            if t<K:chosen=t
            else:
                chosen=0;top=-1e100
                for i in range(K):
                    v=ys[i]/yn[i]+np.sqrt(L/(2*yn[i]))-c[i]
                    if v>top:chosen=i;top=v
        else:
            if t<K:chosen=t
            else:
                chosen=0;top=-1e100
                for i in range(K):
                    v=s[i]/n[i]+np.sqrt(L/(2*n[i]))-g*c[i]
                    if v>top:chosen=i;top=v
        audit=(method==5) or ((method==0 or method==4) and t<B)
        y=np.random.random()<mu[chosen]
        u=np.random.random()
        z=(u>=fn[chosen]) if y else (u<fp[chosen])
        n[chosen]+=1;s[chosen]+=z
        if audit:
            yn[chosen]+=1;ys[chosen]+=y;audits+=1
            agree+=1 if y==z else -1
        regret+=best-(mu[chosen]-c[chosen])
        if cp<3 and t+1==checkpoints[cp]:
            trace[cp,0]=regret;trace[cp,1]=audits;trace[cp,2]=regret+a*audits;cp+=1
    # Report the estimate after the last update, including a final-round audit.
    if method in (0,4,5):
        g=.25 if audits==0 else min(1.,max(.25,agree/audits))
    return trace, g


def config(name,T,D,h=0.1,sign=-1,B=None,K=2,stress=0.):
    g=.5+sign*h
    if K==2:
        mu=np.array([.5,.5+D/(2*g)])
        c=np.array([0,D])
    else:
        c=np.linspace(0,D,K)
        mu=.5+c+np.linspace(-.06,.06,K)
    fp=np.full(K,(1-g)/2);fn=fp.copy()
    if stress:
        # Explicit action-dependent deviation from nominal channel.
        # It makes the costly arm appear worse; absolute deviation is stress.
        fp[0]=max(0,fp[0]-stress);fn[0]=max(0,fn[0]-stress)
        fp[-1]=min(1,fp[-1]+stress);fn[-1]=min(1,fn[-1]+stress)
    if B is None:B=default_budget(T,D,.2)
    return dict(name=name,T=T,D=D,h=h,sign=sign,B=B,K=K,stress=stress,mu=mu,c=c,fp=fp,fn=fn)


def main():
    specs=[]
    for T in [512,2048,8192,32768]:
        for sign in [-1,1]:specs.append(config('horizon',T,.2,sign=sign))
    for B in [0,8,32,128,512,2048,8192]:
        for sign in [-1,1]:specs.append(config('budget',8192,.2,sign=sign,B=B))
    for D in [0,.0125,.025,.05,.1,.2,.25]:
        for sign in [-1,1]:specs.append(config('spread',8192,D,sign=sign))
    for K in [2,4,8,16,32]:specs.append(config('arms',8192,.2,K=K))
    for eps in [0,.03,.06,.12,.2]:specs.append(config('misspecification',8192,.2,stress=eps))
    out=ROOT/'results';out.mkdir(exist_ok=True)
    manifest={k:v for k,v in dict(seeds=256,seed_start=1720406,methods=METHODS,audit_price=.2,
               note='Synthetic Bernoulli trials; no language models queried.',
               configs=[{k:(v.tolist() if isinstance(v,np.ndarray) else v) for k,v in s.items()} for s in specs]).items()}
    (out/'experiment-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    fields=['suite','T','D','h','sign','B','K','stress','method','seed','at','execution_regret','audits','total_regret','final_scale']
    started=time.time()
    with (out/'runs.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
        for no,cfg in enumerate(specs):
            for mid,method in enumerate(METHODS):
                # Oracle-scale control assumes a shared channel; exclude it where violated.
                if cfg['stress'] and mid==1:continue
                for seed in range(1720406,1720406+256):
                    traces,g=simulate(cfg['mu'],cfg['c'],cfg['fp'],cfg['fn'],cfg['T'],cfg['B'],.2,seed,mid)
                    for j,at in enumerate([cfg['T']//4,cfg['T']//2,cfg['T']]):
                        row={k:cfg[k] for k in ['T','D','h','sign','B','K','stress']}
                        row.update(suite=cfg['name'],method=method,seed=seed,at=at,
                            execution_regret=traces[j,0],audits=int(traces[j,1]),total_regret=traces[j,2],final_scale=g)
                        writer.writerow(row)
            f.flush()
            print(f"Completed configuration {no+1}/{len(specs)} ({time.time()-started:.1f}s)",flush=True)
    manifest['elapsed_seconds']=time.time()-started
    manifest['runs_sha256']=hashlib.sha256((out/'runs.csv').read_bytes()).hexdigest()
    (out/'experiment-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')

if __name__=='__main__':main()
