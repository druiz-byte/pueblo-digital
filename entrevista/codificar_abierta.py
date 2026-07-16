# -*- coding: utf-8 -*-
"""Codifica las respuestas ABIERTAS de 'tres problemas de Euskadi' en categorías
y muestra el % de personas que menciona cada una (umbral configurable, def. 10%).
Multi-respuesta: una persona puede caer en varias categorías.

Uso:  python codificar_abierta.py resultados/abierta_problemas_XXXX.json [umbral]
      python codificar_abierta.py --selftest
"""
import json, sys, re, unicodedata, collections
from pathlib import Path

def norm(s):
    s = unicodedata.normalize('NFKD', s or '')
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s.lower()

# Palabras/raíces por categoría (se buscan como subcadena sobre texto normalizado)
CATS = {
 "Vivienda": ["vivienda","alquiler","hipoteca","pisos","okupa","inmobiliari","casero","desahucio","precio de la casa","precio de las casas","etxebizitza","alokairu"],
 "Problemas ligados al mercado del trabajo": ["paro","desempleo","empleo","trabajo","laboral","precari","salario","sueldo","contrato","temporalidad","despido","langabezia","lanpostu"," lana ","enplegu","soldata"],
 "Sanidad, Osakidetza, Salud": ["sanidad","osakidetza","salud","sanitari","medic","hospital","lista de espera","listas de espera","atencion primaria","ambulatorio","osasun"],
 "Delincuencia e inseguridad ciudadana": ["delincuencia","inseguridad","robo","criminalidad","seguridad ciudadana","atraco","hurto","vandalismo","bandas","delinkuentzia","segurtasun"],
 "Inmigración y problemas relacionados con ella": ["inmigra","migrant","migracion","extranjer","refugiad","patera","mena ","etorkin","immigra"],
 "Problemas económicos": ["economi","economic","inflacion","subida de precios","subida de los precios","subiendo los precios","suben los precios","coste de la vida","coste de vida","carestia","poder adquisitivo","pobreza","encarecimiento","situacion economica","nivel de vida","mas caro","muy caro","todo caro","esta todo caro","cada vez mas caro","carisimo","prezio","garestitze","bizi-kostu"],
}
REFUSAL = ["no lo se","no lo sabria","no sabria","no sabria decir","ns/nc","no contesto","prefiero no contestar","no tengo opinion","no tengo ni idea","no sabe no contesta","ninguno en particular","no me interesa la politica"]

def codificar(texto):
    t = norm(texto).strip()
    if not t:
        return set(), True  # vacío -> NS/NC
    cats = set()
    for cat, kws in CATS.items():
        if any(norm(k) in t for k in kws):
            cats.add(cat)
    if cats:
        return cats, False
    # sin categorías sustantivas: NS solo si es rechazo explícito o texto muy corto
    if len(t) < 12 or any(norm(p) in t for p in REFUSAL):
        return set(), True
    return set(), False  # sin código (otros: euskera, corrupción, política...)

def informe(results, umbral=10.0):
    n = len(results)
    counts = collections.Counter()
    ns = 0; uncoded = 0; multi = []
    for r in results:
        cats, es_ns = codificar(r.get('respuesta',''))
        if es_ns:
            ns += 1
        elif not cats:
            uncoded += 1
        for c in cats: counts[c] += 1
        multi.append(len(cats))
    counts["No sabe, no contesta"] = ns
    filas = sorted(counts.items(), key=lambda x:-x[1])
    out = []
    out.append(f"Respuestas: {n} · media de categorías/persona: {sum(multi)/n:.2f} · sin codificar (texto no encaja): {100*uncoded/n:.1f}%\n")
    out.append(f"Categorías mencionadas por ≥{umbral:.0f}% de la población (% de personas que la mencionan):\n")
    out.append("| Categoría | % personas | (n) |")
    out.append("|---|---:|---:|")
    for c,k in filas:
        pct=100*k/n
        if pct>=umbral:
            out.append(f"| {c} | {pct:.1f}% | {k} |")
    out.append("\n_Multi-respuesta: los % suman más de 100 porque cada persona puede mencionar varios problemas._")
    return '\n'.join(out)

def selftest():
    ej=[
      "Para mí lo más grave es el precio de la vivienda y el alquiler, y también el paro juvenil.",
      "La sanidad está fatal, las listas de espera de Osakidetza son enormes. Y la inseguridad.",
      "La inmigración descontrolada, la delincuencia y la subida de precios.",
      "No lo sé, la verdad.",
      "El euskera y la relación con España.",  # no encaja en las 6 -> uncoded
      "",  # NS
    ]
    res=[{'respuesta':x} for x in ej]
    print(informe(res, umbral=0))

if __name__ == '__main__':
    if '--selftest' in sys.argv:
        selftest(); sys.exit()
    path=sys.argv[1]; umbral=float(sys.argv[2]) if len(sys.argv)>2 else 10.0
    d=json.load(open(path,encoding='utf-8'))
    res=d.get('results',d)
    rep=informe(res, umbral)
    print(rep)
    md=Path(path).with_suffix('').name
    outmd=Path(path).parent/f"codificacion_{md}.md"
    outmd.write_text("# Codificación abierta — tres problemas de Euskadi\n\nPregunta: "+d.get('pregunta','')+"\n\n"+rep+"\n", encoding='utf-8')
    print("\n→", outmd)
