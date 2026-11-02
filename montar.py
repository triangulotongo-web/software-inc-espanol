"""Monta Localization/Español a partir de English/*.tyd y las traducciones de trozos/.
Uso: python montar.py [--instalar]   (--instalar lo copia también a la carpeta del juego)"""
import glob, json, os, shutil, sys
import extraer

AQUI = os.path.dirname(os.path.abspath(__file__))
JUEGO = r"C:\Program Files (x86)\Steam\steamapps\common\Software Inc"
IDIOMA = "Español"
META = f'''Name "{IDIOMA}"
Author "Pulsa Start (pulsastart.es)"
Description "Traducción no oficial al español de España. https://github.com/triangulotongo-web/software-inc-espanol"
'''


def de_linea(s):
    out, i = [], 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            out.append({"n": "\n", "t": "\t", "\\": "\\"}.get(s[i + 1], "\\" + s[i + 1]))
            i += 2
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def citar(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("#", "\\#") + '"'


def main():
    textos = json.load(open(os.path.join(AQUI, "textos.json"), encoding="utf-8"))
    es = {}
    for r in glob.glob(os.path.join(AQUI, "trozos", "t*_es.txt")):
        for l in open(r, encoding="utf-8-sig").read().split("\n"):
            i, _, t = l.partition("\t")
            if i.strip().isdigit() and t.strip():
                es[textos[int(i)]] = de_linea(t.rstrip("\r"))
    salida = os.path.join(AQUI, "Localization", IDIOMA)
    shutil.rmtree(salida, ignore_errors=True)
    os.makedirs(salida)
    hechas = faltan = 0
    for f in sorted(glob.glob(os.path.join(AQUI, "English", "*.tyd"))):
        doc = open(f, encoding="utf-8").read()
        partes, pos = [], 0
        for i, j, citado, texto in extraer.traducibles(doc):
            tr = es.get(texto)
            if tr is None:
                faltan += 1
                continue
            hechas += 1
            if citado:
                i, j = i - 1, j + 1  # sustituye también las comillas
            partes += [doc[pos:i], citar(tr)]
            pos = j
        partes.append(doc[pos:])
        open(os.path.join(salida, os.path.basename(f)), "w", encoding="utf-8", newline="").write("".join(partes))
    open(os.path.join(salida, "meta.tyd"), "w", encoding="utf-8").write(META)
    print(f"{hechas} textos traducidos, {faltan} sin traducir")
    if "--instalar" in sys.argv:
        dst = os.path.join(JUEGO, "Localization", IDIOMA)
        shutil.rmtree(dst, ignore_errors=True)
        shutil.copytree(salida, dst)
        print("instalado en", dst)


if __name__ == "__main__":
    main()
