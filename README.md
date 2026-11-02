# Software Inc. en español

Traducción no oficial al **español** de [Software Inc.](https://store.steampowered.com/app/362620/Software_Inc/) (Coredumping), hecha por fans.

| | |
|---|---|
| **Idioma** | Español de España |
| **Versión del juego** | **Beta 1.8.42** (Steam build 24837201) |
| **Versión de la traducción** | 1.0.0 |
| **Funciona con** | El sistema de idiomas del propio juego, sin mods ni programas extra |

## Qué se traduce

- Menús, ventanas, columnas, botones, avisos y ayudas
- Los 37 tutoriales
- Mobiliario y salas
- Tipos de software, categorías y características
- Rasgos de los empleados, tareas, logros y noticias de prensa

En total son **4.660 textos**. Los nombres de empresas inventadas, marcas y personas se quedan como en el original.

**No se traduce** la campaña con Bob (las conversaciones de las misiones): el juego no la carga de los archivos de idioma sino de sus propios datos, y cambiarla obligaría a parchear el juego en cada actualización. Algún texto suelto que el juego tiene escrito directamente en su código también puede salir en inglés.

## Instalación

1. Descarga este repositorio (botón verde **Code → Download ZIP**) o el ZIP de la última versión en [Releases](../../releases).
2. Copia la carpeta `Localization/Español` dentro de la carpeta `Localization` del juego, de forma que quede así:
   `C:\Program Files (x86)\Steam\steamapps\common\Software Inc\Localization\Español\UI.tyd`
   (Si la carpeta `Localization` no existe, abre el juego una vez y ciérralo: la crea al arrancar.)
3. Abre el juego y en las opciones, en **Translations**, elige **Español**.

Para quitarla, borra la carpeta `Localization\Español` y vuelve a elegir English.

> Si tras una actualización del juego aparecen textos en inglés, deja activada en las opciones la casilla *Fallback to English* («Recurrir al inglés», viene activada) y avísanos para ponerla al día.

## Cómo se hizo

Los scripts están en la raíz del repositorio:

- `sacar_ingles.py`: saca con UnityPy los 8 archivos de idioma en inglés (`.tyd`) que el juego lleva dentro.
- `tyd.py`: lector mínimo del formato TyD que localiza cada texto sin tocar las claves ni la estructura.
- `extraer.py`: junta los textos (sin repetidos) y los parte en trozos de `trozos/`.
- `validar.py`: comprueba que cada traducción conserva las marcas del juego: `{0}`, `{KeyBind:…}`, `{H:…}`, plurales `[Mes|Meses]`, etiquetas `<b>` y saltos de línea.
- `montar.py`: reconstruye cada `.tyd` con los textos en español en `Localization/Español` (con `--instalar` lo copia también al juego).

Este repositorio **no incluye ningún archivo del juego**, solo las traducciones.

## Corregir textos

Las traducciones están en `trozos/tNN_es.txt`, una línea por texto (`id<TAB>texto`, con `\n` para los saltos de línea). Corrige ahí, ejecuta `python validar.py` y `python montar.py`, o abre un *issue* con el texto que quieres cambiar.

---

Hecho por [Pulsa Start](https://pulsastart.es/traducciones/). Software Inc. pertenece a Coredumping; esta traducción es gratuita y no oficial.
