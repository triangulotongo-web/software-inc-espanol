"""Comprueba los trozos traducidos: mismos ids y mismas marcas del juego.
Uso: python validar.py [trozos/t00 ...]   (sin argumentos, todos)"""
import glob, os, re, sys
from collections import Counter

AQUI = os.path.dirname(os.path.abspath(__file__))
LLAVE = re.compile(r"\{[^{}]*\}")
# Dentro de estas llaves el texto tras los dos puntos se traduce; del resto se compara todo
ARG_LIBRE = re.compile(r"^\{(H|Warning|\d+:Plural|\d+:Vowel|\d+:FirstOrCount|\d+:NotNull):")
OTRAS = re.compile(r"\[[^\[\]|]*\|[^\[\]]*\]|</?[A-Za-z][^>]*>|\\n")


def marcas(s):
    m = [ARG_LIBRE.match(x).group(0) if ARG_LIBRE.match(x) else x for x in LLAVE.findall(s)]
    m += ["[a|b]" if x.startswith("[") else x.lower() for x in OTRAS.findall(s)]
    return Counter(m)


def leer(ruta):
    d = {}
    for l in open(ruta, encoding="utf-8-sig").read().split("\n"):
        if l.strip():
            i, _, t = l.partition("\t")
            d[i.strip()] = t
    return d


def validar(base):
    en = leer(base + "_en.txt")
    if not os.path.exists(base + "_es.txt"):
        return ["falta el _es.txt"]
    es = leer(base + "_es.txt")
    f = []
    for i, t in en.items():
        if i not in es:
            f.append(f"{i}: falta")
        elif marcas(t) != marcas(es[i]):
            f.append(f"{i}: marcas distintas\n  en: {t[:300]}\n  es: {es[i][:300]}")
    f += [f"{i}: id que no está en el original" for i in es.keys() - en.keys()]
    return f


bases = [os.path.join(AQUI, a.removesuffix("_en.txt").removesuffix("_es.txt")) for a in sys.argv[1:]] or \
    sorted(p[:-7] for p in glob.glob(os.path.join(AQUI, "trozos", "t*_en.txt")))
mal = 0
for b in bases:
    f = validar(b)
    mal += bool(f)
    print(f"{os.path.basename(b)}: {'OK' if not f else str(len(f)) + ' fallos'}")
    for x in f[:40]:
        print("  " + x)
sys.exit(1 if mal else 0)
