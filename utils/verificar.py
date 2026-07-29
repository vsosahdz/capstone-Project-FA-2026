"""
Autoverificación de los ejercicios del curso.

Uso desde un notebook:

    from utils.verificar import verificar
    verificar("1.3", dim_cc)

Cómo funciona y por qué así:

* Se compara una HUELLA HASHEADA del resultado, no el resultado. Así este
  archivo no contiene ninguna respuesta legible: puedes abrirlo sin hacerte
  trampa.

* La huella es TOLERANTE. Solo mira número de filas, el conjunto de nombres
  de columna (sin importar el orden) y la suma de las columnas numéricas
  redondeada a dos decimales. NO mira dtypes, ni el orden de las filas, ni el
  índice, ni la precisión completa de punto flotante.

  El motivo es práctico: un verificador que marca ❌ una respuesta correcta
  destruye la confianza del grupo en treinta segundos, y a partir de ahí nadie
  vuelve a mirar el indicador.

* Como se hashea el RESULTADO y no el código, dos caminos distintos que llegan
  al mismo resultado pasan los dos. Si tu forma de resolverlo no es la misma
  que la del instructor pero llegas al mismo dato, cuenta como correcta.

* No hay acceso a red. Los hashes vienen precomputados abajo.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

# ─────────────────────────────────────────────────────────────────────────
# Textos de diagnóstico
#
# Solo se muestran al FALLAR. La pista que orienta antes de intentar vive en
# la celda Markdown del notebook; esto es lo otro: qué salió mal.
#
# Los marcadores {n} y {esperado} se sustituyen por los valores reales.
# ─────────────────────────────────────────────────────────────────────────

DIAGNOSTICOS: dict[str, str] = {
    "1.2": "No recibí un DataFrame. ¿Asignaste el resultado de read_csv a la variable?",
    "1.3": "Los acentos salieron corruptos. La codificación que usaste decodifica, "
           "pero no es la correcta para este origen. Revisa la tabla de codificaciones.",
    "1.5": "La suma de la columna no coincide. Si te dio unas 100 veces más de lo "
           "esperado, borraste la coma decimal en lugar de convertirla en punto.",
    "1.7": "Te quedaron {n:,} filas y se esperaban {esperado:,}. Si te quedaron más, "
           "drop_duplicates() sin subset no los ve: la columna cargado_en es distinta "
           "entre el original y la recarga. Si te quedaron menos, tu subset es "
           "demasiado corto y borraste asientos legítimos.",
    "1.8": "Tu código está bien. El problema son los datos: conservaste {n:,} filas "
           "de {esperado:,}, así que {perdidas:,} llaves no hacen match. Mira de "
           "cerca los valores de centro_costo en las dos tablas. ¿Son idénticos?",
    "1.9": "Sigues perdiendo filas: {n:,} de {esperado:,}. ¿Aplicaste la "
           "normalización en AMBAS tablas, o solo en una?",
    "2.2": "Obtuviste {n:,} filas y se esperaban {esperado:,}. Si son más, tu rango "
           "incluye meses fuera de abril–junio.",
    "2.4": "El número de filas no coincide: {n:,} en vez de {esperado:,}. Si "
           "obtuviste 8, agrupaste solo por centro de costo y falta la dimensión "
           "temporal.",
    "2.6": "Tu resultado tiene {n:,} filas y se esperaban {esperado:,}. Cuando falta "
           "una llave en el ON, cada fila de un lado hace match con varias del otro "
           "y el resultado se multiplica. ¿Cuántas llaves pusiste?",
    "2.7": "Las cifras no cuadran. Si el sobregasto te sale negativo, invertiste el "
           "orden de la resta. Si el porcentaje no coincide, revisa sobre qué base "
           "lo estás calculando.",
    "3.6": "Tu tabla tiene {n:,} filas y se esperaban {esperado:,}. Si tiene 8, no "
           "recortaste. Si el orden es ascendente, los primeros son los que menos "
           "importan.",
    "3.9": "Falta una de las dos versiones en tu tabla comparativa, o los totales no "
           "corresponden a los dos reportes.",
    "3.11": "El archivo no quedó como se esperaba. Si lo escribiste en utf-8 sin BOM, "
            "Power BI en Windows lo leerá como cp1252 y verás 'NÃ³mina Indirecta' en "
            "lugar de 'Nómina Indirecta'.",
    "R1": "Tus totales no cuadran. Verificaste duplicados en hechos_gasto… "
          "¿revisaste también presupuesto?",
    "R2": "La desviación te salió negativa, como si hubiera un ahorro. Eso es "
          "exactamente lo que verías con datos sucios. ¿Terminaste el paso 1?",
    "R3": "Agrupaste por centro de costo. Esa pregunta ya la respondiste en el caso "
          "principal; esta es otra: te preguntan CUÁNDO empezó.",
    "R4": "Falta el archivo de salida o no tiene las columnas esperadas.",
}

# Ejercicios cuya verificación es PARCIAL: se comprueba una parte y hay otra
# que no se puede calificar. El ✅ debe declararlo, o el participante creerá
# que se validó algo que nadie miró.
PARCIALES: dict[str, str] = {
    "3.6": "El título del gráfico no se califica — compáralo con la solución al cierre.",
}

# Ejercicios del reto, para el resumen de entrega
PASOS_RETO = {
    "R1": "Paso 1 · carga y limpieza",
    "R2": "Paso 2 · desviación por mes",
    "R3": "Paso 3 · gráfico e insight",
    "R4": "Paso 4 · reporte exportado",
}

# ─────────────────────────────────────────────────────────────────────────
# Huellas esperadas.
# Generadas por scripts/generar_hashes.py a partir de los notebooks maestros.
# No se editan a mano.
# ─────────────────────────────────────────────────────────────────────────

HUELLAS: dict[str, dict[str, Any]] = {}

try:  # pragma: no cover
    from utils._huellas import HUELLAS as _H
    HUELLAS = _H
except Exception:
    pass


# ─────────────────────────────────────────────────────────────────────────
# Cálculo de la huella
# ─────────────────────────────────────────────────────────────────────────

def _es_dataframe(obj: Any) -> bool:
    return hasattr(obj, "columns") and hasattr(obj, "shape")


def _perfil(obj: Any) -> dict[str, Any]:
    """
    Reduce el objeto a las invariantes que sí se comparan.

    Deliberadamente NO se incluyen: dtypes, orden de filas, índice, ni floats
    con precisión completa.
    """
    if _es_dataframe(obj):
        columnas = sorted(str(c) for c in obj.columns)
        sumas = {}
        for col in obj.columns:
            serie = obj[col]
            try:
                if serie.dtype.kind in "ifu":
                    sumas[str(col)] = round(float(serie.sum()), 2)
            except AttributeError:
                continue
        return {
            "tipo": "dataframe",
            "filas": int(obj.shape[0]),
            "columnas": columnas,
            "sumas": {k: sumas[k] for k in sorted(sumas)},
        }

    if isinstance(obj, (int, float)):
        return {"tipo": "numero", "valor": round(float(obj), 2)}

    if isinstance(obj, str):
        return {"tipo": "texto", "valor": obj.strip()}

    if isinstance(obj, (list, tuple, set)):
        return {"tipo": "coleccion",
                "valores": sorted(str(v).strip() for v in obj)}

    return {"tipo": "otro", "valor": str(obj)}


def _huella(obj: Any) -> str:
    perfil = _perfil(obj)
    crudo = json.dumps(perfil, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(crudo.encode("utf-8")).hexdigest()[:16]


# ─────────────────────────────────────────────────────────────────────────
# Presentación
# ─────────────────────────────────────────────────────────────────────────

_ANCHO = 66
_ESTADO: dict[str, bool] = {}


def _linea(car: str = "─") -> str:
    return car * _ANCHO


def _forma(perfil: dict[str, Any]) -> str:
    if perfil["tipo"] == "dataframe":
        return f"{perfil['filas']:,} filas · {len(perfil['columnas'])} columnas"
    if perfil["tipo"] == "numero":
        return f"{perfil['valor']:,.2f}"
    if perfil["tipo"] == "coleccion":
        return f"{len(perfil['valores'])} elementos"
    return str(perfil.get("valor", ""))[:40]


def verificar(ejercicio: str, resultado: Any) -> bool:
    """
    Compara `resultado` con la huella esperada del ejercicio e imprime el
    veredicto. Devuelve True si es correcto (útil para el resumen del reto).
    """
    # Modo recolección: lo usa scripts/generar_hashes.py al ejecutar los
    # notebooks de soluciones. En lugar de comparar, registra la huella.
    if os.environ.get("VERIFICAR_MODO") == "recolectar":
        return _recolectar(ejercicio, resultado)

    esperado = HUELLAS.get(ejercicio)

    if esperado is None:
        print(f"⚠️  No hay huella registrada para el ejercicio {ejercicio}.")
        print("    Avisa al instructor: es un problema del material, no tuyo.")
        return False

    perfil = _perfil(resultado)
    correcto = _huella(resultado) == esperado["huella"]
    _ESTADO[ejercicio] = correcto

    if correcto:
        print(_linea("═"))
        print(f"  ✅  Ejercicio {ejercicio} correcto      {_forma(perfil)}")
        if ejercicio in PARCIALES:
            print(f"  ⚠️   {PARCIALES[ejercicio]}")
        print(_linea("═"))
        return True

    # ── Falla: forma obtenida vs esperada, y el diagnóstico ──
    contexto = {
        "n": perfil.get("filas", 0),
        "esperado": esperado.get("filas", 0),
        "perdidas": max(0, esperado.get("filas", 0) - perfil.get("filas", 0)),
    }
    try:
        diagnostico = DIAGNOSTICOS.get(ejercicio, "").format(**contexto)
    except (KeyError, IndexError):
        diagnostico = DIAGNOSTICOS.get(ejercicio, "")

    print(_linea("═"))
    print(f"  ❌  Ejercicio {ejercicio} — aún no")
    print(_linea())
    print(f"  Obtuviste:  {_forma(perfil)}")
    if esperado.get("forma"):
        print(f"  Se esperaba: {esperado['forma']}")
    if diagnostico:
        print(_linea())
        for i, linea in enumerate(_envolver(diagnostico, _ANCHO - 6)):
            print(f"  💡 {linea}" if i == 0 else f"     {linea}")
    print(_linea("═"))
    return False


def _recolectar(ejercicio: str, resultado: Any) -> bool:
    """
    Registra la huella del ejercicio en el archivo apuntado por
    VERIFICAR_SALIDA. Solo se usa durante la autoría del curso.
    """
    destino = Path(os.environ.get("VERIFICAR_SALIDA", "huellas_recolectadas.json"))
    datos = {}
    if destino.exists():
        datos = json.loads(destino.read_text(encoding="utf-8"))
    perfil = _perfil(resultado)
    datos[ejercicio] = {
        "huella": _huella(resultado),
        "filas": perfil.get("filas", 0),
        "forma": _forma(perfil),
    }
    destino.write_text(json.dumps(datos, indent=2, ensure_ascii=False),
                       encoding="utf-8")
    print(f"  📌 recolectado {ejercicio}: {_forma(perfil)}")
    return True


def _envolver(texto: str, ancho: int) -> list[str]:
    palabras, lineas, actual = texto.split(), [], ""
    for p in palabras:
        if len(actual) + len(p) + 1 > ancho:
            lineas.append(actual)
            actual = p
        else:
            actual = f"{actual} {p}".strip()
    if actual:
        lineas.append(actual)
    return lineas


# ─────────────────────────────────────────────────────────────────────────
# Resumen de entrega del reto
# ─────────────────────────────────────────────────────────────────────────

def resumen_reto() -> str:
    """
    Imprime el marcador del reto y devuelve el código de entrega.

    El código se deriva de los resultados: dos participantes con los mismos
    aciertos obtienen el mismo código, y basta cambiar un resultado para que
    cambie. Sirve para que el instructor valide sin abrir el notebook.
    """
    aciertos = 0
    print(_linea("═"))
    print("  RESUMEN DE TU RETO".center(_ANCHO))
    print(_linea("═"))
    for paso, etiqueta in PASOS_RETO.items():
        estado = _ESTADO.get(paso)
        marca = "✅" if estado else ("❌" if estado is False else "⬜")
        if estado:
            aciertos += 1
        print(f"  {etiqueta:<34} {marca}")
    print(_linea())

    firma = "".join("1" if _ESTADO.get(p) else "0" for p in PASOS_RETO)
    codigo = hashlib.sha256(firma.encode()).hexdigest()[:8].upper()
    codigo = f"RETO-{codigo[:4]}-{codigo[4:]}"
    print(f"  {aciertos} / {len(PASOS_RETO)}   ·   código: {codigo}")
    print(_linea("═"))
    print("  Envía este código junto con salidas/reto_reporte.csv")
    return codigo
