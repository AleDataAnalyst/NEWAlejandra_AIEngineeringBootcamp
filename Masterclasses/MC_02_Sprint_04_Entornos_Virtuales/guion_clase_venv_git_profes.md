# Escaleta de clase — Entornos Virtuales + Práctica Git
**Duración total: 2h** | **Fecha: 25 jun 2026**

---

## Setup previo (antes de empezar)

```bash
mkdir ~/demo-venv && cd ~/demo-venv
touch app.py
```

`app.py`:
```python
import requests
print(requests.get("https://httpbin.org/get").status_code)
```

---

## BLOQUE 1 — Entornos Virtuales (30')
> Mostrar el notebook `entornos_virtuales.ipynb` en pantalla. Ir sección a sección.

---

**§1 — ¿Qué es un entorno virtual?** *(~5')*
- Explicar el problema del entorno global
- 🖥️ **DEMO:** `pip list` en tu terminal global — mostrar el caos
- Lanzar la analogía de la despensa

---

**§2 — Crear y activar con `venv`** *(~10')*
- 🖥️ **DEMO en `~/demo-venv`:**
```bash
python3 -m venv .venv
source .venv/bin/activate   # señalar el (.venv) en el prompt
which python3 && pip list   # entorno limpio
pip install requests
python3 app.py              # → 200
deactivate                  # prompt vuelve a normal
python3 -c "import requests"  # → ModuleNotFoundError (si no está global)
```
- Mencionar los comandos de Windows de la sección (sin demo)

---

**§3 — Instalar paquetes** *(~2')*
- Ya cubierto en la demo anterior, repasar `pip install`, `pip show`, `pip uninstall`

---

**§4 — `requirements.txt`** *(~7')*
- 🖥️ **DEMO:**
```bash
source .venv/bin/activate
pip install numpy pandas
pip freeze > requirements.txt && cat requirements.txt
# Simular colega:
cd ~ && mkdir demo-venv-colega && cd demo-venv-colega
python3 -m venv .venv && source .venv/bin/activate
pip install -r ~/demo-venv/requirements.txt
pip list   # idéntico al original
```

---

**§5 — Entornos y Git** *(~3')*
- 🖥️ **DEMO:**
```bash
cd ~/demo-venv
du -sh .venv/          # mostrar cuánto pesa
echo ".venv/" >> .gitignore
```
- Regla de oro: `.venv/` en gitignore, `requirements.txt` en el repo

---

**§6 y §7 — Versiones de Python + Alternativas** *(~3')*
- Solo comentar la tabla del notebook, sin demo
- Destacar conda para el bootcamp

---

## BLOQUE 2 — Presentación del ejercicio Git (~8')
> Guión verbal. Decirlo antes de abrir las breakout rooms.

---

"Muy bien, cerramos la parte de entornos virtuales. Aislar, instalar, documentar — guardad ese esquema.

Ahora vamos con la práctica de Git que nos quedó pendiente la última sesión. Vamos a hacer el ejercicio integrador, y lo vamos a hacer exactamente como se trabaja en un equipo real: cada une en su ordenador, con un repo compartido en GitHub, ramas en paralelo y un hotfix de urgencia por medio.

El contexto es sencillo: vais a crear un repo que se llama `tienda-online`. No hay código Python — son ficheros de texto, para que el foco esté cien por cien en Git y no en entender el código.

Vais a trabajar en parejas. Dentro de cada pareja hay una Persona A y una Persona B, y cada una tiene un rol distinto:

- **Persona A** crea el repo en GitHub, lo configura y añade a B como colaborador. A trabaja en la rama `feature/productos`: crea un fichero con productos y hace dos commits.

- **Persona B** clona el repo y trabaja en paralelo en `feature/carrito` — al mismo tiempo que A, sin esperar.

Hasta aquí es un flujo normal de equipo. Pero entonces pasa algo: A descubre que hay un precio mal puesto en producción. Tiene que hacer un **hotfix** — crear una rama desde `main`, corregirlo, fusionarlo tanto en `main` como en `develop`, y etiquetarlo con una versión. Eso es lo que hace un equipo profesional ante un bug urgente.

B, antes de fusionar su rama, tiene que hacer `git pull` para traerse el hotfix. Si no lo hace, puede haber conflicto.

Al final, los dos ejecutáis `git log --oneline --graph --all` y veréis toda la historia del repo: las dos ramas en paralelo, el hotfix, los tags de versión. Ese grafo es exactamente lo que verías en el día a día de cualquier empresa.

Os paso los pasos por el chat ahora mismo — leedlos antes de empezar. Tenéis **80 minutos**. No hace falta llegar al paso 11; lo importante es que los dos hayáis creado vuestras ramas, hecho commits reales y entendido qué pasa cuando sincronizáis con el repo del compañere.

Cualquier duda, al chat o salís de la sala. Nos vemos en 80 minutos para revisar algún repo en directo."

→ **Pegar pasos en el chat → abrir breakout rooms**

---

*Al volver (puesta en común, ~10'):*
- Pedir a una pareja que comparta pantalla
- Ejecutar `git log --oneline --graph --all` en directo
- Comentar el grafo: ramas, hotfix, tags

---

## PASOS DEL EJERCICIO — para pegar en el chat

```
EJERCICIO GIT — TIENDA ONLINE
Reparto: Persona A y Persona B

SETUP (A hace esto, B espera):
1. A: crea repo "tienda-online" en GitHub (vacío, sin README)
2. A: clona en local → git clone <url>
3. A: crea README.md → git add . && git commit -m "feat: init repo" && git push
4. A: crea rama develop → git checkout -b develop && git push -u origin develop
5. A: añade a B como colaborador (GitHub > Settings > Collaborators)
6. B: clona el repo → git clone <url>

EN PARALELO:
7a. A: git checkout -b feature/productos (desde develop)
    → crea productos.txt con 3 productos
    → git commit -m "feat(productos): add initial product list"
    → añade descripciones → git commit -m "feat(productos): add product descriptions"
    → git push -u origin feature/productos
    → abre PR en GitHub: feature/productos → develop → merge

7b. B: git checkout -b feature/carrito (desde develop)
    → crea carrito.txt → git commit -m "feat(carrito): add shopping cart logic"
    → git push -u origin feature/carrito
    (espera a que A haga el merge del hotfix antes de abrir la PR)

HOTFIX (A):
8. A: git checkout main
   git checkout -b hotfix/precio-erroneo
   → modifica productos.txt (corrige un precio)
   → git commit -m "fix(productos): correct price for product A"
   → merge a main: git checkout main && git merge hotfix/precio-erroneo
   → merge a develop: git checkout develop && git merge hotfix/precio-erroneo
   → git push origin main develop
   → git tag -a v1.0.1 -m "hotfix: correct price" && git push origin v1.0.1

CIERRE (B):
9. B: git checkout develop && git pull origin develop
   → git push -u origin feature/carrito
   → abre PR en GitHub: feature/carrito → develop → merge

RELEASE (cualquiera de los dos):
10. git checkout main && git merge develop
    git push origin main
    git tag -a v1.1.0 -m "release: add cart feature" && git push origin v1.1.0

VISUALIZAR:
11. Los dos: git log --oneline --graph --all
```
