"""Saca los 8 .tyd en inglés que el juego lleva en Resources/Localization/English."""
import os, UnityPy
D = r"C:\Program Files (x86)\Steam\steamapps\common\Software Inc\Software Inc_Data"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "English")
os.makedirs(OUT, exist_ok=True)
env = UnityPy.load(D)
ids = {}
for o in env.objects:
    if o.type.name == "ResourceManager":
        for ruta, ptr in o.read_typetree()["m_Container"]:
            if ruta.startswith("localization/english/"):
                ids[ptr["m_PathID"]] = ruta
for o in env.objects:
    if o.type.name == "TextAsset" and o.path_id in ids and o.assets_file.name == "resources.assets":
        d = o.read()
        txt = d.m_Script
        txt = txt.decode("utf-8") if isinstance(txt, bytes) else txt.encode("utf-8", "surrogateescape").decode("utf-8")
        nombre = (getattr(d, "m_Name", None) or d.name) + ".tyd"
        open(os.path.join(OUT, nombre), "w", encoding="utf-8", newline="").write(txt)
        print(ids[o.path_id], nombre, len(txt))
