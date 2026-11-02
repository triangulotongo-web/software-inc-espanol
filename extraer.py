"""Saca los textos de English/*.tyd y los parte en trozos id<TAB>texto para traducir.
Los saltos de línea van como \\n y los tabuladores como \\t."""
import glob, json, os, re
import tyd

AQUI = os.path.dirname(os.path.abspath(__file__))
NO_TRADUCIR = {"Name", "Plural"}  # claves de Item { Name ...; Plural ...; Value ... } y Feature { Name ... }
ESC = {"\\": "\\", '"': '"', "#": "#", ";": ";", "]": "]", "}": "}", "\r": "\r", "n": "\n", "t": "\t"}
TROZO = 450


def desescapar(s):
    return re.sub(r"\\(.)", lambda m: ESC.get(m.group(1), m.group(0)), s, flags=re.S)


def a_linea(s):
    return s.replace("\r\n", "\n").replace("\\", "\\\\").replace("\n", "\\n").replace("\t", "\\t")


def traducibles(doc):
    for i, j, ruta, citado in tyd.valores(doc):
        if ruta[-1] in NO_TRADUCIR or ruta[-1] == "*":
            continue
        if not citado:
            k = j
            while k < len(doc) and doc[k] in " \t\r\n":
                k += 1
            if k < len(doc) and doc[k] == "{":  # Feature { ... }: es estructura, no texto
                continue
        texto = desescapar(doc[i:j])
        if re.search(r"[A-Za-z]", texto):
            yield i, j, citado, texto


def main():
    textos = {}
    for f in sorted(glob.glob(os.path.join(AQUI, "English", "*.tyd"))):
        doc = open(f, encoding="utf-8").read()
        for _, _, _, t in traducibles(doc):
            textos.setdefault(t, len(textos))
    lista = sorted(textos, key=textos.get)
    json.dump(lista, open(os.path.join(AQUI, "textos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    d = os.path.join(AQUI, "trozos")
    os.makedirs(d, exist_ok=True)
    n = 0
    for k in range(0, len(lista), TROZO):
        with open(os.path.join(d, f"t{n:02d}_en.txt"), "w", encoding="utf-8", newline="\n") as f:
            for j in range(k, min(k + TROZO, len(lista))):
                f.write(f"{j}\t{a_linea(lista[j])}\n")
        n += 1
    print(f"{len(lista)} textos únicos, {sum(map(len, lista))} caracteres, {n} trozos")


if __name__ == "__main__":
    main()
