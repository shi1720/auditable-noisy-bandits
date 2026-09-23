#!/usr/bin/env python3
"""Independent audit of accounting, reported aggregates, and KL constants."""
from pathlib import Path
import sys,csv,json,hashlib,math
from collections import defaultdict
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'results/experiment-manifest.json').read_text())
assert hashlib.sha256((ROOT/'results/runs.csv').read_bytes()).hexdigest()==manifest['runs_sha256']
groups=defaultdict(list);count=0;seen=set()
def group_key(r):
 return (r['suite'],int(r['T']),float(r['D']),float(r['h']),int(r['sign']),int(r['B']),int(r['K']),float(r['stress']),r['method'])
with (ROOT/'results/runs.csv').open() as f:
 for r in csv.DictReader(f):
  count+=1
  assert abs(float(r['total_regret'])-float(r['execution_regret'])-.2*int(r['audits']))<1e-8
  assert 0<=int(r['audits'])<=int(r['at'])
  assert float(r['execution_regret'])>=-1e-8
  k=tuple(r[x] for x in ['suite','T','D','h','sign','B','K','stress','method','seed','at'])
  assert k not in seen;seen.add(k)
  if r['at']==r['T']:
   expected=int(r['T']) if r['method']=='Audit-all UCB' else int(r['B']) if r['method'] in ('SC-UCB','Audit-only ETC') else 0
   assert int(r['audits'])==expected
   key=group_key(r)
   groups[key].append(float(r['total_regret']))
assert count==208896 and len(groups)==272
for v in groups.values():assert len(v)==256
with (ROOT/'results/summary.csv').open() as f:
 for r in csv.DictReader(f):
  key=group_key(r)
  vs=groups[key];m=math.fsum(vs)/len(vs)
  se=math.sqrt(math.fsum((x-m)**2 for x in vs)/(len(vs)-1)/len(vs))
  assert abs(m-float(r['total_regret_mean']))<1e-8
  assert abs(se-float(r['total_regret_se']))<1e-8
assert F(36,5)*F(256,225)+F(256,39)<16
# KL evaluated without calling the package joint-law or KL implementations.
max_ratio=0.;checks=0
for d0 in range(1,26):
 D=d0/100
 for j in range(1,126):
  h=j/1000
  for arm in [0,1]:
   worlds=[]
   for sign in [-1,1]:
    g=.5+sign*h;mu=.5 if arm==0 else .5+D/(2*g);match=(1+g)/2
    worlds.append([(1-mu)*match,(1-mu)*(1-match),mu*(1-match),mu*match])
   for p,q in (worlds,worlds[::-1]):
    divergence=math.fsum(x*math.log(x/y) for x,y in zip(p,q))
    max_ratio=max(max_ratio,divergence/h**2);assert divergence<=16*h*h+1e-13;checks+=1
report={'policy_runs':count//3,'rows':count,'summary_groups':len(groups),'seeds_per_group':256,
'joint_KL_grid_checks':checks,'largest_observed_KL_over_h_squared':max_ratio,
'exact_KL_bound_constant':str(F(36,5)*F(256,225)+F(256,39)),
'checks':'PASS','scope':'Internal verification; grid checks are not proofs.'}
(ROOT/'results/verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
