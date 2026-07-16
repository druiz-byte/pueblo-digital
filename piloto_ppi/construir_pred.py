# -*- coding: utf-8 -*-
"""Predictor-sustituto sin API: empareja cada encuestado real con el panel v2 por
voto x ideologia (x sexo), con back-off, y devuelve la respuesta del panel a Q0 (p18)."""
import glob, json, numpy as np, pyreadstat
from collections import defaultdict

BASE='/sessions/optimistic-awesome-brown/mnt/Pueblo digital'
OPC=['Muy buena','Buena','Regular','Mala','Muy mala','No lo sé / prefiero no contestar']
LET={c:o for c,o in zip('ABCDEF',OPC)}

def voto_c_panel(v):
    return {'PNV/EAJ':'PNV','EH Bildu':'BILDU','PSE-EE':'PSE','Elkarrekin Podemos':'UP','Sumar':'UP',
            'PP':'PP','Vox':'VOX','Otra candidatura':'OTROS','Voto nulo':'OTROS','Voto en blanco':'OTROS',
            'Abstención':'ABST','No sabe / No contesta':'NS'}.get(v,'NS')
def voto_c_sav(code):
    return {1:'PNV',2:'BILDU',3:'PSE',4:'UP',5:'UP',6:'PP',7:'VOX',8:'OTROS',9:'OTROS',10:'OTROS',
            11:'ABST',12:'NS',13:'NS'}.get(int(code) if code==code else -1,'NS')
def ideo_t(x):
    if x is None or x!=x or x==99: return 'NS'
    x=float(x)
    return 'IZQ' if x<=3 else ('CEN' if x<=6 else 'DCHA')

def cargar():
    SAV=glob.glob('/sessions/optimistic-awesome-brown/mnt/uploads/*.sav')[0]
    df,meta=pyreadstat.read_sav(SAV)
    lab=meta.variable_value_labels['p18']
    sexomap={1:'Hombre',2:'Mujer'}
    real=[]
    for _,r in df.iterrows():
        real.append({'y':lab.get(r['p18']),'sexo':sexomap.get(r['sexo']),
                     'voto':voto_c_sav(r['p45']),'ideo':ideo_t(r['p36'])})
    # panel + ideologia por id
    ag={a['id']:a for a in json.load(open(f'{BASE}/pv_agentes_v2.json'))['poblacion']}
    panel=json.load(open(f'{BASE}/entrevista/resultados/encuesta_2026-07-14_164342.json'))['results']
    cell=defaultdict(list); bvi=defaultdict(list); bv=defaultdict(list); bi=defaultdict(list); allp=[]
    for p in panel:
        ans=LET.get(p['resps'].get('0'))
        if ans is None: continue
        vc=voto_c_panel(p['voto']); it=ideo_t(ag[p['id']].get('ideologia_0_10'))
        cell[(vc,it,p['genero'])].append(ans); bvi[(vc,it)].append(ans)
        bv[vc].append(ans); bi[it].append(ans); allp.append(ans)
    pools=(cell,bvi,bv,bi,allp)
    return real, pools, OPC

def pool_for(r, pools):
    cell,bvi,bv,bi,allp=pools
    for key,d in ((( r['voto'],r['ideo'],r['sexo']),cell),((r['voto'],r['ideo']),bvi),
                  ((r['voto'],),bv),((r['ideo'],),bi)):
        k = key[0] if len(key)==1 else key
        pool = d.get(k)
        if pool: return pool
    return allp

def construir_f(real, pools, seed):
    rng=np.random.default_rng(seed); f=[]
    for r in real:
        pool=pool_for(r,pools); f.append(pool[rng.integers(len(pool))])
    return np.array(f,dtype=object)
