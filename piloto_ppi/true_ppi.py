# -*- coding: utf-8 -*-
"""PPI++ con predicción GENERATIVA directa (f_i = LLM sobre el perfil real del encuestado i),
emparejada 1:1 con Y_i. Bloque 5. Compara con el sustituto por emparejamiento demográfico."""
import glob, json, numpy as np, pyreadstat
from ppi_engine import estimar_opcion, estimar_media

BASE='/sessions/optimistic-awesome-brown/mnt/Pueblo digital'
PRED=json.load(open(f'{BASE}/entrevista/predicciones_deusto_bloque5.json'))
SAV=glob.glob('/sessions/optimistic-awesome-brown/mnt/uploads/*.sav')[0]
df,meta=pyreadstat.read_sav(SAV)
df=df.set_index(df['id'].astype(int))
tmpl=json.load(open(f'{BASE}/entrevista/encuestas/barometro_digital_5_politica_democracia.json'))['preguntas']
def qidx(sub):
    for i,q in enumerate(tmpl):
        if sub.lower() in q['texto'].lower(): return i
ids=[int(k) for k in PRED.keys() if int(k) in df.index]
print(f"emparejados 1:1: {len(ids)} encuestados\n")

def letter_num(L):  # 0-10: A=0..K=10
    i='ABCDEFGHIJK'.find(L) if L else -1; return float(i) if i>=0 else None

NS=[50,100,150,200,250]; SEEDS=range(60); alpha=0.05

# ================= A) p18 categórica =================
OPC=['Muy buena','Buena','Regular','Mala','Muy mala','No lo sé / prefiero no contestar']
LET={c:o for c,o in zip('ABCDEF',OPC)}
lab18=meta.variable_value_labels['p18']; q18=str(qidx('situación política general'))
Y=[]; F=[]
for i in ids:
    y=lab18.get(df.loc[i,'p18']); f=LET.get(PRED[str(i)].get(q18))
    if y is None or f is None: continue
    Y.append(y); F.append(f)
Y=np.array(Y,dtype=object); F=np.array(F,dtype=object)
theta={c:float((Y==c).mean()) for c in OPC}
fdist={c:float((F==c).mean()) for c in OPC}
print("A) p18 — real vs predicción generativa (imputación) vs |sesgo|:")
for c in OPC: print(f"   {c:34} real {100*theta[c]:5.1f}%  pred {100*fdist[c]:5.1f}%  |sesgo| {100*abs(fdist[c]-theta[c]):4.1f}")
# concordancia individual
print(f"   concordancia individual (pred==real): {100*np.mean(F==Y):.1f}%")

print(f"\n   {'n':>4} | cobPPI cobCLA | anchoPPI anchoCLA red%")
for n in NS:
    if n>=len(Y): continue
    wp=[];wc=[];cp=[];cc=[]
    for s in SEEDS:
        rng=np.random.default_rng(s); idx=rng.permutation(len(Y)); lab,unl=idx[:n],idx[n:]
        for c in OPC:
            r=estimar_opcion(Y[lab],F[lab],F[unl],c,alpha)
            wp.append(r['ppi_ancho']);wc.append(r['clasico_ancho'])
            cp.append(r['ppi_lo']<=theta[c]<=r['ppi_hi']);cc.append(r['clasico_lo']<=theta[c]<=r['clasico_hi'])
    print(f"   {n:>4} | {100*np.mean(cp):5.1f}% {100*np.mean(cc):5.1f}% | {100*np.mean(wp):7.2f} {100*np.mean(wc):7.2f} {100*(1-np.mean(wp)/np.mean(wc)):4.1f}")

# ================= B) escalas 0-10 medias =================
BQ={'Democracia Euskadi (p20_2)':('Euskadi','p20_2'),
    'Confianza Gobierno Vasco (p21_6)':('Gobierno Vasco','p21_6'),
    'Confianza Gobierno Central (p21_1)':('Gobierno Central','p21_1'),
    'Confianza partidos (p21_13)':('partidos políticos','p21_13')}
print("\nB) escalas 0-10 (media). corr generativa vs corr emparejado (piloto previo):")
corr_prev={'p20_2':0.225,'p21_6':0.283,'p21_1':-0.003,'p21_13':0.066}
for name,(sub,sv) in BQ.items():
    qi=str(qidx(sub)); Yb=[];Fb=[]
    for i in ids:
        y=df.loc[i,sv]; f=letter_num(PRED[str(i)].get(qi))
        if y!=y or y==99 or f is None: continue
        Yb.append(float(y)); Fb.append(f)
    Yb=np.array(Yb); Fb=np.array(Fb); th=float(Yb.mean())
    corr=float(np.corrcoef(Yb,Fb)[0,1])
    print(f"\n{name}: n={len(Yb)} real={th:.2f} pred={Fb.mean():.2f} (sesgo {Fb.mean()-th:+.2f})")
    print(f"   corr(Y,f): generativa {corr:+.3f}  |  emparejado {corr_prev[sv]:+.3f}")
    print(f"   {'n':>4} | cobPPI | anchoPPI anchoCLA red%  | n_efic")
    for n in NS:
        if n>=len(Yb): continue
        wp=[];wc=[];cp=[]
        for s in SEEDS:
            rng=np.random.default_rng(100+s); idx=rng.permutation(len(Yb)); lab,unl=idx[:n],idx[n:]
            r=estimar_media(Yb[lab],Fb[lab],Fb[unl],alpha)
            wp.append(r['ppi_ancho']);wc.append(r['clasico_ancho']);cp.append(r['ppi_lo']<=th<=r['ppi_hi'])
        red=100*(1-np.mean(wp)/np.mean(wc)); neff=n/max(1e-9,(1-red/100)**2)
        print(f"   {n:>4} | {100*np.mean(cp):5.1f}% | {np.mean(wp):7.3f} {np.mean(wc):7.3f} {red:4.1f} | {neff:5.0f}")
