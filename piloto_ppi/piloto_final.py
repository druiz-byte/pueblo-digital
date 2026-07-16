# -*- coding: utf-8 -*-
"""PILOTO PPI++ — Bloque 5 (política). Datos reales Deustobarómetro verano 2026 (n=1000).
Parte A: p18 (categórica) -> proporciones por opción.
Parte B: escalas 0-10 -> medias (democracia y confianza institucional).
Predictor f: panel v2 emparejado por voto x ideología x sexo (sustituto sin API)."""
import glob, json, numpy as np, pyreadstat
from collections import defaultdict
from ppi_engine import estimar_opcion, estimar_media
from construir_pred import voto_c_panel, voto_c_sav, ideo_t

BASE='/sessions/optimistic-awesome-brown/mnt/Pueblo digital'
SAV=glob.glob('/sessions/optimistic-awesome-brown/mnt/uploads/*.sav')[0]
df,meta=pyreadstat.read_sav(SAV)
ag={a['id']:a for a in json.load(open(f'{BASE}/pv_agentes_v2.json'))['poblacion']}
panel=json.load(open(f'{BASE}/entrevista/resultados/encuesta_2026-07-14_164342.json'))['results']
tmpl=json.load(open(f'{BASE}/entrevista/encuestas/barometro_digital_5_politica_democracia.json'))['preguntas']
def qidx(sub):
    for i,q in enumerate(tmpl):
        if sub.lower() in q['texto'].lower(): return i
NS=[50,100,150,200,300,500]; SEEDS=range(40); alpha=0.05
def cellkey(vc,it,sx): return (vc,it,sx)

# ===================== PARTE A: p18 categórica =====================
OPC=['Muy buena','Buena','Regular','Mala','Muy mala','No lo sé / prefiero no contestar']
LET={c:o for c,o in zip('ABCDEF',OPC)}
lab18=meta.variable_value_labels['p18']
realA=[{'y':lab18.get(r['p18']),'vc':voto_c_sav(r['p45']),'it':ideo_t(r['p36']),
        'sx':{1:'Hombre',2:'Mujer'}.get(r['sexo'])} for _,r in df.iterrows()]
cA=defaultdict(list); cbvi=defaultdict(list); cbv=defaultdict(list); allA=[]
for p in panel:
    a=LET.get(p['resps'].get(str(qidx('situación política general'))))
    if a is None: continue
    vc=voto_c_panel(p['voto']); it=ideo_t(ag[p['id']].get('ideologia_0_10'))
    cA[(vc,it,p['genero'])].append(a); cbvi[(vc,it)].append(a); cbv[vc].append(a); allA.append(a)
def poolA(r): return cA.get((r['vc'],r['it'],r['sx'])) or cbvi.get((r['vc'],r['it'])) or cbv.get(r['vc']) or allA
YA=np.array([r['y'] for r in realA],dtype=object)
thetaA={c:float((YA==c).mean()) for c in OPC}
def fA(seed):
    rng=np.random.default_rng(seed); return np.array([poolA(r)[rng.integers(len(poolA(r)))] for r in realA],dtype=object)

resA={}
for n in NS:
    acc={c:defaultdict(list) for c in OPC}
    for s in SEEDS:
        rng=np.random.default_rng(9000+s); f=fA(s); idx=rng.permutation(len(YA)); lab,unl=idx[:n],idx[n:]
        for c in OPC:
            r=estimar_opcion(YA[lab],f[lab],f[unl],c,alpha); tt=thetaA[c]
            acc[c]['w_ppi'].append(r['ppi_ancho']); acc[c]['w_cl'].append(r['clasico_ancho'])
            acc[c]['cov_ppi'].append(r['ppi_lo']<=tt<=r['ppi_hi']); acc[c]['cov_cl'].append(r['clasico_lo']<=tt<=r['clasico_hi'])
    resA[n]={c:{k:float(np.mean(v)) for k,v in acc[c].items()} for c in OPC}
imp_A={c:float(np.mean([fA(s)==c for s in range(10)])) for c in OPC}  # imputación (marginal panel)

# ===================== PARTE B: escalas 0-10 (medias) =====================
def L2N(L):
    i='ABCDEFGHIJK'.find(L) if L else -1; return float(i) if i>=0 else None
BQ={'Democracia Euskadi (p20_2)':'Euskadi','Confianza Gobierno Vasco (p21_6)':'Gobierno Vasco',
    'Confianza Gobierno Central (p21_1)':'Gobierno Central','Confianza partidos (p21_13)':'partidos políticos'}
SAVVAR={'Democracia Euskadi (p20_2)':'p20_2','Confianza Gobierno Vasco (p21_6)':'p21_6',
        'Confianza Gobierno Central (p21_1)':'p21_1','Confianza partidos (p21_13)':'p21_13'}
resB={}
for name,sub in BQ.items():
    qi=qidx(sub); sv=SAVVAR[name]
    cB=defaultdict(list); bvi=defaultdict(list); bv=defaultdict(list); allB=[]
    for p in panel:
        v=L2N(p['resps'].get(str(qi)))
        if v is None: continue
        vc=voto_c_panel(p['voto']); it=ideo_t(ag[p['id']].get('ideologia_0_10'))
        cB[(vc,it,p['genero'])].append(v); bvi[(vc,it)].append(v); bv[vc].append(v); allB.append(v)
    real=[]
    for _,r in df.iterrows():
        y=r[sv]
        if y!=y or y==99: continue
        vc=voto_c_sav(r['p45']); it=ideo_t(r['p36']); sx={1:'Hombre',2:'Mujer'}.get(r['sexo'])
        pool=cB.get((vc,it,sx)) or bvi.get((vc,it)) or bv.get(vc) or allB
        real.append((float(y),float(np.mean(pool))))
    real=np.array(real); Yb=real[:,0]; Fb=real[:,1]; theta=float(Yb.mean())
    perN={}
    for n in NS:
        w_ppi=[]; w_cl=[]; cov_ppi=[]; cov_cl=[]; e_ppi=[]; e_cl=[]
        for s in SEEDS:
            rng=np.random.default_rng(7000+s); idx=rng.permutation(len(Yb)); lab,unl=idx[:n],idx[n:]
            r=estimar_media(Yb[lab],Fb[lab],Fb[unl],alpha)
            w_ppi.append(r['ppi_ancho']); w_cl.append(r['clasico_ancho'])
            cov_ppi.append(r['ppi_lo']<=theta<=r['ppi_hi']); cov_cl.append(r['clasico_lo']<=theta<=r['clasico_hi'])
            e_ppi.append(abs(r['ppi_pt']-theta)); e_cl.append(abs(r['clasico_pt']-theta))
        perN[n]=dict(w_ppi=float(np.mean(w_ppi)),w_cl=float(np.mean(w_cl)),
                     cov_ppi=float(np.mean(cov_ppi)),cov_cl=float(np.mean(cov_cl)),
                     red=100*(1-np.mean(w_ppi)/np.mean(w_cl)),
                     e_ppi=float(np.mean(e_ppi)),e_cl=float(np.mean(e_cl)))
    resB[name]=dict(theta=theta,imput=float(Fb.mean()),sesgo_imput=float(Fb.mean()-theta),
                    corr=float(np.corrcoef(Yb,Fb)[0,1]),perN=perN)

json.dump(dict(pA=dict(theta=thetaA,imput=imp_A,res=resA),pB=resB),
          open('resultado_piloto_final.json','w'),ensure_ascii=False,indent=1)

# ---- salida ----
print("="*70,"\nPARTE A — p18 situación política PV (proporciones). Verdad n=1000:")
for c in OPC: print(f"  {c:34} real {100*thetaA[c]:5.1f}%   panel(imput) {100*imp_A[c]:5.1f}%   |sesgo| {100*abs(imp_A[c]-thetaA[c]):4.1f} pp")
print(f"\n  {'n':>4} | cobPPI cobCLA | anchoPPI anchoCLA red%")
for n in NS:
    R=resA[n]; cov_ppi=np.mean([R[c]['cov_ppi'] for c in OPC]); cov_cl=np.mean([R[c]['cov_cl'] for c in OPC])
    wp=np.mean([R[c]['w_ppi'] for c in OPC]); wc=np.mean([R[c]['w_cl'] for c in OPC])
    print(f"  {n:>4} | {100*cov_ppi:5.1f}% {100*cov_cl:5.1f}% | {100*wp:7.2f} {100*wc:7.2f} {100*(1-wp/wc):4.1f}")

print("\n"+"="*70,"\nPARTE B — escalas 0-10 (media poblacional):")
for name,d in resB.items():
    print(f"\n{name}: real={d['theta']:.2f}  imput.panel={d['imput']:.2f} (sesgo {d['sesgo_imput']:+.2f})  corr(Y,f)={d['corr']:+.3f}")
    print(f"  {'n':>4} | cobPPI cobCLA | anchoPPI anchoCLA red%  | n_efic")
    for n in NS:
        p=d['perN'][n]; red=p['red']; neff=n/max(1e-9,(1-red/100)**2)
        print(f"  {n:>4} | {100*p['cov_ppi']:5.1f}% {100*p['cov_cl']:5.1f}% | {p['w_ppi']:7.3f} {p['w_cl']:7.3f} {red:4.1f} | {neff:5.0f}")
print("\n(n_efic = tamaño real que necesitaría el clásico para igualar el IC de PPI++)")
