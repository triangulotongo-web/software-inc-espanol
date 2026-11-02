# Encargo de traducción (Software Inc.)

Traduces al español de España los textos del juego Software Inc. (simulador de empresa de software: empleados, oficinas, proyectos, marketing, bolsa…).
Carpeta: C:\Users\trian\Desktop\retcheno\softwareinc-es\trozos

Cada trozo `tNN_en.txt` tiene una línea por texto: `id<TAB>texto en inglés`. Los saltos de línea dentro de un texto aparecen como `\n` (barra + n) y los tabuladores como `\t`.
Escribe `tNN_es.txt` en la misma carpeta con EXACTAMENTE los mismos ids, en el mismo orden, formato `id<TAB>traducción`, una línea por id (UTF-8).
Mantén los `\n` (mismo número) y no metas saltos de línea reales. Trozos grandes: escríbelos por partes (Write la primera y luego `cat >> archivo <<'EOF'` con Bash) sin dejarte ids.

Marcas del juego:
- `{0}`, `{1}`, `{0:ToLower}`, `{KeyBind:ContextMenu}`, `{Currency:50000}`, `{0:PluralKey:Room}`: cópialas tal cual.
- `{H:Continue}` resalta un texto: deja `{H:` y traduce lo de dentro como se llame ese botón/ventana en español (`{H:Continuar}`).
- `{0:Plural:employees,employee}` → traduce las dos formas (plural,singular): `{0:Plural:empleados,empleado}`. Igual con `{0:Vowel:an,a}` (pon la forma española, p. ej. `{0:Vowel:un,un}`), `{0:FirstOrCount:...}` y `{0:NotNull:...}`: conserva el prefijo hasta los dos puntos y traduce el resto.
- `[Month|Months]` es singular|plural: `[Mes|Meses]`. Mantén los corchetes y la barra.
- Etiquetas `<b>`, `</b>`, `<color=...>`: iguales.
- No uses comillas dobles " ; usa « » o comillas simples.

Estilo: español de España, natural, con el humor del original cuando lo hay. Textos de interfaz cortos (botones, columnas) deben quedar cortos.
Términos: employee = empleado, designer = diseñador, programmer = programador, artist = artista, marketing = marketing,
release = lanzamiento/lanzar, review = reseña, bug = error (bug si es jerga), feature = característica, deal = acuerdo,
contract = contrato, office = oficina, room = sala, furniture = mobiliario, server = servidor, framework = framework,
operating system = sistema operativo, add-on = complemento, stock/shares = acciones, loan = préstamo, IP = IP (propiedad intelectual),
skill = habilidad, specialization = especialización, team = equipo, leader = líder, salary = sueldo, revenue = ingresos.
Nombres propios de empresas inventadas, marcas o personas: igual.

Al terminar cada trozo comprueba (desde la carpeta softwareinc-es):
  python validar.py trozos/tNN
y corrige hasta que diga OK. Responde al final solo con la lista de trozos y si quedaron OK.
