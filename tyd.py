"""Lector mínimo de TyD (el formato de Software Inc) que devuelve dónde está cada valor de texto,
para poder sustituir solo los valores y dejar intactos los nombres, la estructura y los comentarios."""


def _espacio(doc, p):
    while p < len(doc):
        if doc[p].isspace():
            p += 1
        elif doc[p] == "#":
            while p < len(doc) and doc[p] != "\n":
                p += 1
        else:
            break
    return p


def _simbolo(doc, p):
    i = p
    while p < len(doc) and not doc[p].isspace() and doc[p] not in '{}[];"#*':
        p += 1
    return doc[i:p], p


def valores(doc):
    """Lista de (inicio, fin, ruta, citado). doc[inicio:fin] es el texto tal cual está en el archivo
    (sin comillas si es citado). ruta es la tupla de nombres de los padres y el propio."""
    res = []

    def bloque(p, ruta, con_nombres):
        while True:
            p = _espacio(doc, p)
            if p >= len(doc):
                return p
            c = doc[p]
            if c == ";":
                p += 1
                continue
            if c in "}]":
                return p
            nombre = None
            if con_nombres:
                nombre, p = _simbolo(doc, p)
                p = _espacio(doc, p)
            while doc[p] == "*":  # atributos *clave valor
                _, p = _simbolo(doc, p + 1)
                p = _espacio(doc, p)
                if doc[p] not in "*#{":
                    p = _valor(p, ruta + ("*",))
                    p = _espacio(doc, p)
            r = ruta + (nombre,)
            if doc[p] == "{":
                p = bloque(p + 1, r, True)
                assert doc[p] == "}", f"esperaba }} en {p}"
                p += 1
            elif doc[p] == "[":
                p = bloque(p + 1, r, False)
                assert doc[p] == "]", f"esperaba ] en {p}"
                p += 1
            else:
                p = _valor(p, r)

    def _valor(p, ruta):
        if doc[p] == '"':
            i = p + 1
            p = i
            while not (doc[p] == '"' and doc[p - 1] != "\\"):
                p += 1
            res.append((i, p, ruta, True))
            return p + 1
        i = p
        while p < len(doc) and doc[p] not in "\r\n;{*#}]" or (p > i and doc[p - 1] == "\\" and doc[p] not in "\r\n"):
            p += 1
        fin = p
        while fin > i and doc[fin - 1] in " \t":
            fin -= 1
        res.append((i, fin, ruta, False))
        return p

    bloque(0, (), True)
    return res
