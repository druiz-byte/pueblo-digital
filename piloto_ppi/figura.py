# -*- coding: utf-8 -*-
import json, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
d=json.load(open('resultado_piloto_final.json'))
OPC=['Muy buena','Buena','Regular','Mala','Muy mala','NS/NC']
KEYS=list(d['pA']['theta'].keys())
real=[100*d['pA']['theta'][k] for k in KEYS]
imp =[100*d['pA']['imput'][k] for k in KEYS]
NS=[50,100,150,200,300,500]

fig,(ax1,ax2)=plt.subplots(1,2,figsize=(13.5,5.3))
# ---- A: p18 real vs imputacion ingenua ----
x=np.arange(len(OPC)); w=0.38
ax1.bar(x-w/2, real, w, label='Real (Deustobarómetro)', color='#2b6cb0')
ax1.bar(x+w/2, imp,  w, label='Panel como verdad (imputación ingenua)', color='#e07b39')
ax1.set_xticks(x); ax1.set_xticklabels(OPC, rotation=25, ha='right', fontsize=9)
ax1.set_ylabel('% de respuestas'); ax1.set_title('A. p18 «situación política del País Vasco»\nla sustitución ingenua se equivoca hasta 43 p.p.')
ax1.legend(fontsize=8.5); ax1.grid(axis='y',alpha=.3)
for xi,(r,i) in enumerate(zip(real,imp)):
    ax1.annotate(f'{abs(i-r):.0f}',(xi,max(r,i)+1),ha='center',fontsize=8,color='#a33')

# ---- B: reduccion de IC vs n (PPI++ se adapta a la calidad del predictor) ----
col={'Confianza Gobierno Vasco (p21_6)':'#2f855a','Democracia Euskadi (p20_2)':'#38a169',
     'Confianza partidos (p21_13)':'#a0aec0','Confianza Gobierno Central (p21_1)':'#cbd5e0'}
for name,dd in d['pB'].items():
    red=[dd['perN'][str(n)]['red'] for n in NS]
    ax2.plot(NS,red,marker='o',label=f"{name.split('(')[0].strip()} (corr={dd['corr']:+.2f})",color=col.get(name))
ax2.axhline(0,color='k',lw=.8)
ax2.set_xlabel('nº de encuestas reales etiquetadas (n)'); ax2.set_ylabel('reducción del ancho de IC vs clásico (%)')
ax2.set_title('B. Ganancia de PPI++ según cuánto informa el panel\n(power-tuning: nunca por debajo de 0 = nunca peor)')
ax2.legend(fontsize=8); ax2.grid(alpha=.3)
plt.tight_layout(); plt.savefig('piloto_ppi_politica.png',dpi=150,bbox_inches='tight')
print('figura ok')
