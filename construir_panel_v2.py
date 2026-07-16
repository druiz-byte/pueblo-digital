# -*- coding: utf-8 -*-
"""Construye el panel v2 (pv_agentes_v2.json) anclando cada Persona en un
encuestado REAL del Sociómetro Vasco 83 (opción B) e inyectando los bloques de
medios/bienestar (ESS España) y capital social (EUSTAT Capital Social 2022)
mediante emparejamiento estadístico por celda con 5-6 llaves.

Solo procesa datos (no usa la API). El barómetro se lanza aparte con
lanzar_barometro_v2.py.

Requisitos: pip install pyreadstat openpyxl
Uso:  python construir_panel_v2.py
"""
import json, random, csv
from pathlib import Path
from collections import defaultdict
import pyreadstat, openpyxl

random.seed(2026)
BASE = Path(__file__).parent
SV   = BASE / "Datos sociómetro GobEsp" / "24sv83_etik.sav"
ESS  = BASE / "Datos ESS" / "ESS country data - ES.csv"
CS   = BASE / "datos capital social 2022" / "MICRODATOS_ECS22.XLSX"
OUT  = BASE / "pv_agentes_v2.json"
N    = 1000

# ── nombres por lengua/género ───────────────────────────────────────────────
NOM_EUS_H = ["Jon","Mikel","Iker","Unai","Ander","Aitor","Julen","Ibai","Eneko","Gorka","Asier","Xabier","Beñat","Igor","Peru"]
NOM_EUS_M = ["Ane","Maialen","Nerea","Leire","Irati","Naroa","Ainhoa","June","Uxue","Amaia","Nahia","Garazi","Oihana","Maddi","Enara"]
NOM_ES_H  = ["Javier","Carlos","Antonio","Manuel","Francisco","Jesús","Ángel","Luis","Miguel","Rafael","Fernando","José","David","Sergio","Alberto"]
NOM_ES_M  = ["María","Carmen","Ana","Isabel","Laura","Cristina","Marta","Pilar","Rosa","Elena","Sara","Nuria","Beatriz","Lucía","Teresa"]
APE_EUS = ["Etxeberria","Aguirre","Zubizarreta","Lasa","Goikoetxea","Urrutia","Arrieta","Bilbao","Elorza","Gabilondo","Larrañaga","Mendizabal","Otxoa","Zabala","Iraola"]
APE_ES  = ["García","Fernández","González","Rodríguez","López","Martínez","Sánchez","Pérez","Gómez","Ruiz","Díaz","Moreno","Muñoz","Romero","Ortega"]

def nombre(genero, euskaldun):
    h = genero == "Hombre"
    if euskaldun:
        n = random.choice(NOM_EUS_H if h else NOM_EUS_M); ape = APE_EUS
    else:
        n = random.choice(NOM_ES_H if h else NOM_ES_M); ape = random.choice([APE_EUS, APE_ES])
    a1 = random.choice(ape if isinstance(ape, list) and isinstance(ape[0], str) else APE_ES)
    a2 = random.choice(APE_EUS if euskaldun else APE_ES)
    return n, f"{a1} {a2}"

# ── llaves de armonización ──────────────────────────────────────────────────
def edad_g(a):
    a = int(a)
    return "18-29" if a<30 else "30-44" if a<45 else "45-59" if a<60 else "60-74" if a<75 else "75+"
def ideol_band(x):
    if x is None: return None
    return "izq" if x<=3 else "der" if x>=7 else "centro"

def code(v):
    return None if v is None or (isinstance(v,float) and v!=v) else int(v)
def scale(v, maxv=10):
    v = code(v)
    return v if (v is not None and 0 <= v <= maxv) else None

# ============================================================================
# 1) ANCLA: Sociómetro 83 → remuestreo ponderado de 1000 encuestados reales
# ============================================================================
df, meta = pyreadstat.read_sav(str(SV))
rows = df.to_dict("records")

MAP_ESTUDIOS = {1:"Sin estudios / primarios incompletos",2:"Primarios (EGB/ESO)",3:"Formación Profesional",4:"Bachillerato superior",5:"Universitarios"}
EDU_G        = {1:"bajo",2:"bajo",3:"medio",4:"medio",5:"alto"}
MAP_LABORAL  = {1:"Trabaja (jornada completa)",2:"Trabaja (jornada parcial)",3:"En paro",4:"Labores del hogar",5:"Estudiando",6:"Jubilado/a, pensionista",7:"Otras situaciones",8:"Ns/Nc"}
LAB_G        = {1:"ocupado",2:"ocupado",3:"parado",4:"hogar",5:"estudiante",6:"jubilado",7:"otros",8:"otros"}
MAP_CLASE    = {1:"Media-alta o acomodada",2:"Media-media",3:"Media-baja u obrera",4:"Ns/Nc"}
CLA_G        = {1:"alta",2:"media",3:"baja",4:None}
MAP_EUSK     = {1:"Euskaldun (habla bien)",2:"Euskaldun (habla bastante bien)",3:"Habla algo de euskera",4:"Sabe algunas palabras de euskera",5:"Erdaldun (no habla euskera)",6:"Ns/Nc"}
MAP_PROV     = {1:"Álava",2:"Bizkaia",3:"Gipuzkoa"}
MAP_NAC      = {1:"En el País Vasco",2:"En el País Vasco",3:"En el País Vasco",4:"En Navarra",5:"En el resto de España",6:"En Iparralde (País Vasco francés)",7:"En el extranjero",8:"N/D"}
MAP_VALOR    = {1:"Muy buena",2:"Buena",3:"Mala",4:"Muy mala",5:"Ns/Nc"}
MAP_SALUD    = {1:"Muy buena",2:"Buena",3:"Regular",4:"Mala",5:"Muy mala",6:"Ns/Nc"}
MAP_SEGUR    = {1:"Sí, totalmente seguro",2:"Más bien seguro",3:"Más bien inseguro",4:"Nada seguro",5:"Ns/Nc"}
MAP_INTERES  = {1:"Muy interesado/a",2:"Bastante interesado/a",3:"Poco interesado/a",4:"Nada interesado/a",5:"Ns/Nc"}
MAP_DINERO   = {1:"Muchos problemas para llegar a fin de mes",2:"Algunos problemas para llegar a fin de mes",3:"Sin problemas para llegar a fin de mes",4:"Ns/Nc"}
MAP_INDEP    = {1:"Partidario/a de la independencia del País Vasco",2:"A favor o en contra de la independencia según las circunstancias",3:"No partidario/a de la independencia",4:"Ns/Nc"}
MAP_IDENT    = {1:"Únicamente vasco/a",2:"Más vasco/a que español/a",3:"Tanto vasco/a como español/a",4:"Más español/a que vasco/a",5:"Únicamente español/a",6:"Ns/Nc"}

# Voto: intención 2024 (P21); si NS/NC/Resto, respaldo con recuerdo 2020 (P23)
VOTO_P21 = {1:"PNV/EAJ",2:"EH Bildu",3:"PSE-EE",4:"Elkarrekin Podemos",5:"Sumar",6:"PP",7:"Vox",8:"Otra candidatura",10:"Voto en blanco",11:"Voto nulo"}
VOTO_P23 = {1:"PNV/EAJ",2:"EH Bildu",3:"PSE-EE",4:"Elkarrekin Podemos",5:"PP",6:"Vox",7:"Otra candidatura",9:"Voto en blanco",10:"Voto nulo"}
def voto_de(r):
    # Primario: recuerdo 2020 (P23, voto realizado y más limpio). Respaldo: intención 2024 (P21).
    p21, p23 = code(r["P21"]), code(r["P23"])
    if p23 in VOTO_P23: return VOTO_P23[p23]
    if p21 in VOTO_P21: return VOTO_P21[p21]
    if p23 == 8 or p21 == 9: return "Abstención"
    return "No sabe / No contesta"

weights = [max(0.0, r["wt"]) for r in rows]
sample = random.choices(rows, weights=weights, k=N)

personas = []
for i, r in enumerate(sample, 1):
    gen_code = code(r["P37"]) or code(r["P01"])
    genero = {1:"Hombre",2:"Mujer",3:"No binario"}.get(gen_code,"Mujer")
    eusk_c = code(r["P32"]); euskaldun = eusk_c in (1,2,3)
    nom, ape = nombre(genero, euskaldun)
    edad = code(r["P02"])
    estudios_c = code(r["P33"]); lab_c = code(r["P03"]); clase_c = code(r["P34"])
    ideo = scale(r["P28"])
    p = {
        "id": i, "nombre": nom, "apellidos": ape, "genero": genero,
        "edad": edad, "grupo_edad": edad_g(edad),
        "provincia": MAP_PROV.get(code(r["lurral"]),"País Vasco"),
        "habitat": "Menos de 5.000 hab." if code(r["P0B"])==999 else "5.000 o más hab.",
        "nacimiento": MAP_NAC.get(code(r["P35"]),"N/D"),
        "nivel_estudios": MAP_ESTUDIOS.get(estudios_c,"N/D"),
        "situacion_laboral": MAP_LABORAL.get(lab_c,"N/D"),
        "clase_social": MAP_CLASE.get(clase_c,"N/D"),
        "lengua_encuesta": "Euskera" if code(r["P0A"]) in (1,2) else "Castellano",
        "euskera": MAP_EUSK.get(eusk_c,"N/D"),
        "religion": "No especificada",
        "ideologia_0_10": ideo,
        "escala_nacionalismo_0_10": scale(r["P29"]),
        "identidad": MAP_IDENT.get(code(r["P30"]),"N/D"),
        "preferencia_territorial": MAP_INDEP.get(code(r["P31"]),"N/D"),
        "voto_autonomicas_2024": voto_de(r),
        "valoracion_economia_pv": MAP_VALOR.get(code(r["P08"]),"N/D"),
        "valoracion_politica_pv": MAP_VALOR.get(code(r["P06"]),"N/D"),
        "problemas_dinero": MAP_DINERO.get(code(r["P11"]),"N/D"),
        "salud_ancla": MAP_SALUD.get(code(r["P04"]),"N/D"),
        "seguridad_percibida": MAP_SEGUR.get(code(r["P05"]),"N/D"),
        "interes_politica": MAP_INTERES.get(code(r["P17"]),"N/D"),
        "principales_problemas": [],
        "peso": 1.0,
        "_k": {"sexo": 1 if genero=="Hombre" else 2, "edad_g": edad_g(edad),
               "edu_g": EDU_G.get(estudios_c), "lab_g": LAB_G.get(lab_c),
               "cla_g": CLA_G.get(clase_c), "ideol": ideol_band(ideo),
               "prov": code(r["lurral"])},
    }
    personas.append(p)
print(f"[1] Ancla Sociometro: {len(personas)} Personas remuestreadas de {len(rows)} reales")

# ============================================================================
# 2) DONANTE ESS España → perfil_mediatico + perfil_bienestar
# ============================================================================
def clean(v, lo, hi):
    try: v = float(v)
    except (TypeError, ValueError): return None
    return v if lo <= v <= hi else None

ESS_EDU = {1:"bajo",2:"bajo",3:"medio",4:"medio",5:"alto",6:"alto",7:"alto"}
ESS_LAB = {1:"ocupado",2:"estudiante",3:"parado",4:"parado",5:"otros",6:"jubilado",7:"hogar",8:"otros"}
ess_pool = []
with open(ESS, newline="", encoding="utf-8", errors="replace") as f:
    rd = csv.reader(f); head = next(rd); idx = {h:i for i,h in enumerate(head)}
    for row in rd:
        g = clean(row[idx["gndr"]],1,2); a = clean(row[idx["agea"]],14,110); edu = clean(row[idx["eisced"]],1,7)
        if not (g and a and edu): continue
        ess_pool.append({
            "sexo": int(g), "edad_g": edad_g(a), "edu_g": ESS_EDU.get(int(edu)),
            "lab_g": ESS_LAB.get(int(clean(row[idx["mnactic"]],1,8) or 0)),
            "ideol": ideol_band(clean(row[idx["lrscale"]],0,10)),
            "nwspol": clean(row[idx["nwspol"]],0,1200), "netusoft": clean(row[idx["netusoft"]],1,5),
            "tvtot": clean(row[idx["tvtot"]],0,7), "happy": clean(row[idx["happy"]],0,10),
            "stflife": clean(row[idx["stflife"]],0,10), "health": clean(row[idx["health"]],1,5),
            "sclmeet": clean(row[idx["sclmeet"]],1,7), "fltlnl": clean(row[idx["fltlnl"]],1,4),
            "trstplt": clean(row[idx["trstplt"]],0,10), "trstprl": clean(row[idx["trstprl"]],0,10),
        })
print(f"[2] Donante ESS: {len(ess_pool)} registros validos")

def build_index(pool, keys):
    d = defaultdict(list)
    for r in pool: d[tuple(r[k] for k in keys)].append(r)
    return d
ess_keysets = [("sexo","edad_g","edu_g","lab_g","ideol"),("sexo","edad_g","edu_g","lab_g"),
               ("sexo","edad_g","edu_g"),("sexo","edad_g"),("sexo",)]
ess_idx = [build_index(ess_pool, ks) for ks in ess_keysets]

USO_INTERNET = {1:"Nunca",2:"Rara vez",3:"Algunos días/semana",4:"Casi todos los días",5:"Todos los días"}
SALUD_ESS = {1:"Muy buena",2:"Buena",3:"Regular",4:"Mala",5:"Muy mala"}
CONTACTO  = {1:"Nunca",2:"Menos de una vez al mes",3:"Una vez al mes",4:"Varias veces al mes",5:"Una vez a la semana",6:"Varias veces por semana",7:"A diario"}
SOLEDAD   = {1:"Casi nunca",2:"Alguna vez",3:"A menudo",4:"Casi siempre"}

n_ess = defaultdict(int)
for p in personas:
    d = None
    for ks, idx in zip(ess_keysets, ess_idx):
        cand = idx.get(tuple(p["_k"].get(x) for x in ks))
        if cand: d = random.choice(cand); n_ess[len(ks)] += 1; break
    p["perfil_mediatico"] = {
        "consumo_noticias_min_dia": None if not d else d["nwspol"],
        "uso_internet": None if not d or d["netusoft"] is None else USO_INTERNET.get(int(d["netusoft"])),
        "consumo_tv_franjas": None if not d else d["tvtot"],
        "interes_politica": p["interes_politica"],
        "confianza_politicos_0_10": None if not d else d["trstplt"],
        "confianza_parlamento_0_10": None if not d else d["trstprl"],
    }
    p["perfil_bienestar"] = {
        "felicidad_0_10": None if not d else d["happy"],
        "satisfaccion_vida_0_10": None if not d else d["stflife"],
        "salud_autopercibida": None if not d or d["health"] is None else SALUD_ESS.get(int(d["health"])),
        "contacto_social": None if not d or d["sclmeet"] is None else CONTACTO.get(int(d["sclmeet"])),
        "sentimiento_soledad": None if not d or d["fltlnl"] is None else SOLEDAD.get(int(d["fltlnl"])),
    }
print(f"[2] ESS emparejado por nº de llaves: {dict(sorted(n_ess.items(), reverse=True))}")

# ============================================================================
# 3) DONANTE Capital Social 2022 → perfil_social
# ============================================================================
wb = openpyxl.load_workbook(CS, read_only=True, data_only=True); ws = wb.active
cs_rows = ws.iter_rows(values_only=True); cs_head = [str(c) for c in next(cs_rows)]
ci = {h:i for i,h in enumerate(cs_head)}
CS_PROV = {"01":1,"48":2,"20":3}
CS_EDADG = {1:"18-29",2:"18-29",3:"18-29",4:"30-44",5:"30-44",6:"30-44",7:"45-59",8:"45-59",9:"45-59",10:"60-74",11:"60-74",12:"60-74",13:"75+",14:"75+"}
CS_CLA = {1:"alta",2:"media",3:"baja",4:None}
def gv(row, name):
    try: return float(row[ci["CS1_"+name]])
    except (TypeError, ValueError): return None
cs_pool = []
for row in cs_rows:
    sexo = 1 if str(row[ci["CS1_SEXO"]]).strip()=="1" else 2
    try: edadr = int(row[ci["CS1_EDADR"]])
    except (TypeError, ValueError): continue
    cla = str(row[ci["CS1_CLASER"]]).strip()
    cs_pool.append({
        "sexo": sexo, "edad_g": CS_EDADG.get(edadr), "prov": CS_PROV.get(str(row[ci["CS1_TERH"]]).strip()),
        "cla_g": CS_CLA.get(int(cla)) if cla.isdigit() else None,
        "CONGEN":gv(row,"CONGEN"),"CONINS":gv(row,"CONINS"),"CONPRO":gv(row,"CONPRO"),
        "REDAMP":gv(row,"REDAMP"),"REDPRO":gv(row,"REDPRO"),"AYUEMO":gv(row,"AYUEMO"),
        "INTPOL":gv(row,"INTPOL"),"PARSOC":gv(row,"PARSOC"),"ASOPER":gv(row,"ASOPER"),
        "ASOVOL":gv(row,"ASOVOL"),"COHSOC":gv(row,"COHSOC"),"PROXIM":gv(row,"PROXIM"),
        "SEGUIR":gv(row,"SEGURI"),"CORRUP":gv(row,"CORRUP"),"SATISF":gv(row,"SATISF"),"FELSAL":gv(row,"FELSAL"),
    })
print(f"[3] Donante Capital Social: {len(cs_pool)} registros")
cs_keysets = [("sexo","edad_g","prov","cla_g"),("sexo","edad_g","prov"),("sexo","edad_g"),("sexo",)]
cs_idx = [build_index(cs_pool, ks) for ks in cs_keysets]

n_cs = defaultdict(int)
for p in personas:
    d = None
    for ks, idx in zip(cs_keysets, cs_idx):
        cand = idx.get(tuple(p["_k"].get(x) for x in ks))
        if cand: d = random.choice(cand); n_cs[len(ks)] += 1; break
    p["perfil_social"] = None if not d else {
        "confianza_general_0_10": d["CONGEN"], "confianza_instituciones_0_10": d["CONINS"],
        "confianza_profesiones_0_10": d["CONPRO"], "red_amplia_personas": d["REDAMP"],
        "red_proxima_personas": d["REDPRO"], "apoyo_emocional_0_10": d["AYUEMO"],
        "interes_politico_0_10": d["INTPOL"], "participacion_social_0_10": d["PARSOC"],
        "pertenencia_asociaciones_0_10": d["ASOPER"], "voluntariado_0_10": d["ASOVOL"],
        "cohesion_social_0_10": d["COHSOC"], "sentimiento_proximidad_0_10": d["PROXIM"],
        "seguridad_0_10": d["SEGUIR"], "percepcion_corrupcion_0_10": d["CORRUP"],
        "satisfaccion_vida_ingresos_0_10": d["SATISF"], "felicidad_salud_0_10": d["FELSAL"],
    }
print(f"[3] Capital Social emparejado por nº de llaves: {dict(sorted(n_cs.items(), reverse=True))}")

for p in personas: p.pop("_k", None)
doc = {
    "fuente": "Panel v2 — ancla Sociometro Vasco 83 + ESS Espana + EUSTAT Capital Social 2022",
    "n": N, "territorio": "País Vasco (CAV)",
    "construccion": {
        "metodo": "Anclaje en encuestado real (opcion B) + emparejamiento estadistico multi-llave",
        "ancla": "Sociometro Vasco 83 (remuestreo ponderado por wt)",
        "donante_medios_bienestar": "ESS Espana (kNN por sexo x edad x educacion x laboral x ideologia)",
        "donante_capital_social": "EUSTAT Capital Social 2022 (kNN por sexo x edad x provincia x clase)",
    },
    "poblacion": personas,
}
OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"[4] Escrito {OUT.name} con {len(personas)} Personas")
