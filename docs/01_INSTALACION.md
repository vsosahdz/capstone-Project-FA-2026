# Instalación del entorno

Tiempo estimado: **15–20 minutos**. Sigue los pasos en orden y copia los
comandos tal cual.

Si algo falla, ve directo a [Problemas conocidos](#problemas-conocidos): los
tres errores que ocurren en la práctica están ahí con su solución exacta.

---

## Antes de empezar

Necesitas tres cosas instaladas:

| | Cómo comprobar |
|---|---|
| **Python 3.12** | Abre PowerShell y escribe `py --version` |
| **Visual Studio Code** | Debe abrirse desde el menú Inicio |
| **Extensiones de VS Code** | Python y Jupyter (paso 5) |

---

# Windows

## Paso 1 · Descargar el curso

Abre **PowerShell** y ejecuta:

```powershell
cd $HOME\Documents
git clone https://github.com/<organizacion>/curso-cierre-datos-financieros.git
cd curso-cierre-datos-financieros
```

> Si no tienes `git`, descarga el ZIP del repositorio desde GitHub
> (botón verde **Code** → **Download ZIP**), descomprímelo en
> `Documentos` y entra a la carpeta con `cd`.

## Paso 2 · Crear el entorno virtual

```powershell
py -m venv .venv
```

> ⚠️ Usa **`py`**, no `python`. Ver [problema 1](#problema-1--se-abre-la-microsoft-store).

## Paso 3 · Activar el entorno virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Debe aparecer `(.venv)` al inicio de la línea:

```
(.venv) PS C:\Users\tu-usuario\Documents\curso-cierre-datos-financieros>
```

> ⚠️ Si sale un error rojo sobre "ejecución de scripts", ve al
> [problema 2](#problema-2--no-se-puede-cargar-el-archivo-activateps1). Es el
> error más común en equipos corporativos y se resuelve en un comando.

## Paso 4 · Instalar las librerías

```powershell
pip install -r requirements.txt
```

Tarda entre 1 y 3 minutos. Al final debe decir `Successfully installed…`.

## Paso 5 · Instalar las extensiones de VS Code

```powershell
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
```

O manualmente: abre VS Code, presiona `Ctrl+Shift+X` y busca **Python** y
**Jupyter** (ambas de Microsoft).

## Paso 6 · Abrir el curso en VS Code

```powershell
code .
```

## Paso 7 · Seleccionar el intérprete

Dentro de VS Code:

1. Presiona `Ctrl+Shift+P`
2. Escribe `Python: Select Interpreter` y presiona Enter
3. Elige la opción que contiene **`.venv`**

> ⚠️ Si no aparece ninguna opción con `.venv`, ve al
> [problema 3](#problema-3--vs-code-no-encuentra-el-kernel).

## Paso 8 · Comprobar que todo quedó bien

1. Abre `notebooks/00_verificacion_entorno.ipynb`
2. Ejecuta la única celda con `Shift+Enter`
3. Deben aparecer solo ✅

Si ves algún ❌, el propio resultado te dice a qué problema de esta guía ir.

---

# macOS

Los mismos ocho pasos, con dos comandos distintos. En macOS casi nunca falla.

```bash
# Paso 1 · Descargar el curso
cd ~/Documents
git clone https://github.com/<organizacion>/curso-cierre-datos-financieros.git
cd curso-cierre-datos-financieros

# Paso 2 · Crear el entorno virtual  (python3, no py)
python3.12 -m venv .venv

# Paso 3 · Activar el entorno virtual  (source, no .\Scripts\)
source .venv/bin/activate

# Paso 4 · Instalar las librerías
pip install -r requirements.txt

# Paso 5 · Extensiones de VS Code
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter

# Paso 6 · Abrir el curso
code .
```

Los pasos 7 y 8 son idénticos a Windows, pero el atajo es `Cmd+Shift+P`.

> En macOS no existe el problema 2: no hay política de ejecución que bloquee
> la activación.

---

# Problemas conocidos

## Problema 1 · Se abre la Microsoft Store

**Síntoma:** escribes `python -m venv .venv` y en vez de ejecutarse se abre la
Microsoft Store, o aparece:

```
Python no se encontró; ejecute sin argumentos para instalar desde Microsoft Store
```

**Causa:** Windows trae un `python.exe` señuelo que solo sirve para llevarte a
la tienda.

**Solución:** usa el lanzador `py`, que sí apunta a tu instalación real:

```powershell
py -m venv .venv
```

---

## Problema 2 · No se puede cargar el archivo Activate.ps1

**Síntoma:** al activar el entorno virtual aparece en rojo:

```
.\.venv\Scripts\Activate.ps1 : No se puede cargar el archivo
C:\...\.venv\Scripts\Activate.ps1, porque la ejecución de scripts está
deshabilitada en este sistema.
```

**Causa:** la política de ejecución de PowerShell bloquea scripts. Es el
comportamiento por defecto en equipos corporativos.

**Solución:** ejecuta esto y vuelve a activar:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

> `-Scope Process` aplica **solo a esta ventana de PowerShell**. No cambia la
> configuración del equipo y no requiere permisos de administrador. Si cierras
> la ventana, hay que repetirlo.

**Alternativa** si tampoco te deja: usa el Símbolo del sistema (CMD) en lugar
de PowerShell, donde el comando de activación es:

```
.venv\Scripts\activate.bat
```

---

## Problema 3 · VS Code no encuentra el kernel

**Síntoma:** al abrir un notebook, arriba a la derecha dice *Select Kernel* y
no aparece ninguna opción con `.venv`. O al ejecutar una celda no pasa nada.

**Causa:** falta seleccionar el intérprete, o falta `ipykernel` en el entorno.

**Solución, en este orden:**

1. Confirma que el entorno está activo: debe verse `(.venv)` en la terminal.

2. Instala el kernel dentro del entorno:

   ```powershell
   pip install ipykernel
   ```

3. Selecciona el intérprete:
   `Ctrl+Shift+P` → `Python: Select Interpreter` → la opción con `.venv`

4. Recarga VS Code:
   `Ctrl+Shift+P` → `Developer: Reload Window`

5. En el notebook, arriba a la derecha: **Select Kernel** →
   **Python Environments** → la opción con `.venv`

---

## Problema 4 · pip no puede descargar (proxy o red)

**Síntoma:** `pip install` se queda colgado o dice
`Could not fetch URL … Connection timed out`.

**Solución:** avisa al instructor. En la red de la empresa ya está verificado
que `pip` funciona, así que suele ser un problema de la sesión: reconéctate a
la red corporativa y vuelve a intentar.

---

## Si nada funciona

No te quedes atorado: **puedes seguir el curso completo sin haber terminado
cada bloque**. Cada notebook arranca leyendo un archivo ya preparado en
`datos/checkpoints/`, así que puedes incorporarte en cualquier punto. Avísale
al instructor y continúa.
