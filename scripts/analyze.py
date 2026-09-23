#!/usr/bin/env python3
from pathlib import Path
import csv,json,hashlib
from collections import defaultdict
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.family':'serif','font.size':9,'axes.titlesize':10,'axes.labelsize':9,'legend.fontsize':8,'pdf.fonttype':42,'ps.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.alpha':.16,'figure.constrained_layout.use':True})
COL={'SC-UCB':'#007f83','Oracle-scale UCB':'#313a68','Naive proxy UCB':'#c66322','Rank-only UCB':'#9b497c','Audit-only ETC':'#686868','Audit-all UCB':'#b79442'}
rows=list(csv.DictReader((ROOT/'results/runs.csv').open()))
for r in rows:
 for k in ['T','B','K','seed','at','audits','sign']:r[k]=int(r[k])
 for k in ['D','h','stress','execution_regret','total_regret','final_scale']:r[k]=float(r[k])
final=[r for r in rows if r['at']==r['T']]
keys=['suite','T','D','h','sign','B','K','stress','method']
groups=defaultdict(list)
for r in final:groups[tuple(r[k] for k in keys)].append(r)
summ=[]
for key,rs in groups.items():
 d=dict(zip(keys,key));d['n']=len(rs)
 for metric in ['execution_regret','audits','total_regret','final_scale']:
  v=np.array([r[metric] for r in rs]);d[metric+'_mean']=v.mean();d[metric+'_se']=v.std(ddof=1)/np.sqrt(len(v))
 summ.append(d)
with (ROOT/'results/summary.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(summ[0]));w.writeheader();w.writerows(summ)
def save(name):
 plt.savefig(ROOT/'figures'/f'{name}.pdf',bbox_inches='tight')
 plt.savefig(ROOT/'figures'/f'{name}.png',dpi=180,bbox_inches='tight');plt.close()
def curve(ax,suite,x,metric,method,**filters):
 s=sorted([r for r in summ if r['suite']==suite and r['method']==method and all(r[k]==v for k,v in filters.items())],key=lambda r:r[x])
 xx=np.array([r[x] for r in s]);y=np.array([r[metric+'_mean'] for r in s]);se=np.array([r[metric+'_se'] for r in s])
 ax.plot(xx,y,'o-',ms=3,lw=1.5,label=method,color=COL[method]);ax.fill_between(xx,y-1.96*se,y+1.96*se,color=COL[method],alpha=.12)

# Mechanism: same observable distribution and opposite net-optimal actions.
fig,axs=plt.subplots(1,2,figsize=(6.6,2.45))
g=np.linspace(.25,1,301);D=.2
axs[0].plot(g,np.full_like(g,.5),label='Tool 0: cost 0',color=COL['Oracle-scale UCB'])
axs[0].plot(g,.5+D/(2*g)-D,label='Tool 1: cost 0.2',color=COL['Naive proxy UCB'])
for v in [.4,.6]:axs[0].axvline(v,ls=':',lw=1,color='gray')
axs[0].set(xlabel=r'Unknown evaluator scale $\gamma$',ylabel=r'Net utility $\mu_i-c_i$',title='(a) Identical proxy means: (0.5, 0.6)');axs[0].legend(loc='upper right')
axs[1].bar([0,1],[.5,.6],width=.34,color=COL['Oracle-scale UCB'],label=r'$\gamma=0.4$')
axs[1].bar(np.array([0,1])+.36,[.5,.6],width=.34,color=COL['SC-UCB'],label=r'$\gamma=0.6$')
axs[1].set(xticks=[.18,1.18],xticklabels=['Tool 0','Tool 1'],ylabel='Probability evaluator reports success',ylim=(0,.85),title='(b) Free feedback cannot identify the world');axs[1].legend()
save('01-identification')

fig,axs=plt.subplots(1,2,figsize=(6.6,2.7))
for ax,sign in zip(axs,[-1,1]):
 for method in list(COL)[:5]:curve(ax,'horizon','T','total_regret',method,sign=sign)
 ax.set(xscale='log',yscale='log',xlabel='Horizon T',ylabel='Regret including audit expenditure',title=f"{'(a)' if sign<0 else '(b)'} Scale {0.5+sign*.1:.1f}")
axs[1].legend(loc='upper left',fontsize=7)
save('02-horizon')
fig,axs=plt.subplots(1,2,figsize=(6.6,2.6))
for ax,metric in zip(axs,['execution_regret','total_regret']):
 for method in ['SC-UCB','Audit-only ETC']:
  for sign in [-1,1]:
   s=sorted([r for r in summ if r['suite']=='budget' and r['method']==method and r['sign']==sign],key=lambda r:r['B'])
   x=np.array([r['B'] for r in s]);y=np.array([r[metric+'_mean'] for r in s]);e=np.array([r[metric+'_se'] for r in s])
   ax.plot(x,y,('o-' if sign==-1 else 's--'),color=COL[method],ms=3,label=f'{method}, scale {0.5+sign*.1:.1f}')
   ax.fill_between(x,y-1.96*e,y+1.96*e,color=COL[method],alpha=.1)
 ax.set(xscale='symlog',xlim=(-1,9500),xlabel='Trusted audit budget B',ylabel='Execution regret' if metric=='execution_regret' else 'Regret + 0.2 B',title='(a) Decision error' if metric=='execution_regret' else '(b) Full objective')
axs[0].legend(fontsize=6.8)
save('03-budget')

fig,axs=plt.subplots(1,2,figsize=(6.6,2.55))
for method in ['SC-UCB','Oracle-scale UCB','Audit-only ETC']:
 curve(axs[0],'arms','K','total_regret',method)
axs[0].set(xlabel='Number of tools K',ylabel='Total regret',title='(a) Same audit budget across K',xticks=[2,8,16,32]);axs[0].legend(fontsize=7)
for method in ['SC-UCB','Audit-only ETC','Naive proxy UCB','Rank-only UCB']:
 curve(axs[1],'misspecification','stress','total_regret',method)
axs[1].set(xlabel=r'Action-dependent deviation $\varepsilon$',ylabel='Total regret',title='(b) Violating the shared channel');axs[1].legend(fontsize=7)
save('04-structure-stress')
fig,axs=plt.subplots(1,2,figsize=(6.6,2.5))
for ax,sign in zip(axs,[-1,1]):
 for method in ['SC-UCB','Oracle-scale UCB','Audit-only ETC','Naive proxy UCB','Rank-only UCB']:
  curve(ax,'spread','D','total_regret',method,sign=sign)
 ax.set(xlabel='Execution-price spread D',ylabel='Total regret',title=f"{'(a)' if sign<0 else '(b)'} Scale {0.5+sign*.1:.1f}")
axs[1].legend(fontsize=7)
save('05-spread')
# Theory-only curves, deliberately separate from empirical measurements.
fig,axs=plt.subplots(1,2,figsize=(6.6,2.5))
T=np.logspace(2,8,150);a=.2
for D in [.0,.001,.01,.1]:
 f=np.sqrt(T)+np.minimum(D*T,(a*D*D)**(1/3)*T**(2/3))
 axs[0].plot(T,f,label=f'D={D:g}')
axs[0].set(xscale='log',yscale='log',xlabel='Horizon T',ylabel='Rate expression (constants omitted)',title='(a) Price-sensitive minimax interpolation');axs[0].legend(fontsize=7)
B=np.logspace(0,6,150)
for D in [.001,.01,.1]:axs[1].plot(B,np.sqrt(1e6)+D*1e6/np.sqrt(B+1),label=f'D={D:g}')
axs[1].set(xscale='log',yscale='log',xlabel='Audit budget B',ylabel='Rate expression (constants omitted)',title=r'(b) Budget frontier at $T=10^6$');axs[1].legend(fontsize=7)
save('06-theory-rates')

# TeX table generated exclusively from retained observations.
lines=[r'\begin{tabular}{lrrrr}',r'\toprule',r'& \multicolumn{2}{c}{$\gamma=0.4$} & \multicolumn{2}{c}{$\gamma=0.6$} \\',r'Method & Execution & Total & Execution & Total \\',r'\midrule']
for method in COL:
 cells=[method]
 for sign in [-1,1]:
  r=next(r for r in summ if r['suite']=='horizon' and r['T']==32768 and r['method']==method and r['sign']==sign)
  for m in ['execution_regret','total_regret']:cells.append(f"${r[m+'_mean']:.1f}\\,\\pm\\,{r[m+'_se']:.1f}$")
 lines.append(' & '.join(cells)+r' \\')
lines.extend([r'\bottomrule',r'\end{tabular}'])
(ROOT/'paper/results-table.tex').write_text('\n'.join(lines)+'\n')
print('Policy-environment-seed runs:',len(final))
print('Configurations:',len(set(tuple(r[k] for k in keys[:-1]) for r in summ)))
for r in summ:
 if r['suite'] in ['arms','misspecification'] and r['method'] in ['SC-UCB','Audit-only ETC']:
  print(r['suite'],r['K'],r['stress'],r['method'],round(r['total_regret_mean'],2),round(r['total_regret_se'],2))
