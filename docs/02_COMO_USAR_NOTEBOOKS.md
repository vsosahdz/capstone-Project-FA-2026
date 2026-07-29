# Cómo usar los notebooks

Lee esto una vez antes de empezar. Son tres minutos y te ahorra confusión.

---

## Los dos tipos de celda

### 📖 Celdas de ejemplo

Las ejecuta y explica el instructor. Tú solo las corres con `Shift+Enter` y
observas el resultado.

Vienen **con el resultado ya visible**, así que puedes leerlas incluso sin
ejecutar nada. Sirven de referencia cuando te atores.

### ✏️ Celdas de TU TURNO

Tienen blancos que tienes que completar:

```python
df_q2 = df[df["fecha"].between("______", "______")]
```

**Nunca te piden inventar sintaxis.** El código viene escrito; el blanco cae
siempre en una decisión: qué columna, qué periodo, qué criterio. Eso es lo que
se está practicando.

Arriba de cada turno hay una 💡 **pista**. Empieza por ahí.

---

## La autoverificación

Después de cada turno hay una celda como esta:

```python
verificar("1.3", dim_cc)
```

Ejecútala. Si acertaste:

```
══════════════════════════════════════════════════════════
  ✅  Ejercicio 1.3 correcto      8 filas · 3 columnas
══════════════════════════════════════════════════════════
```

Si no:

```
══════════════════════════════════════════════════════════
  ❌  Ejercicio 1.7 — aún no
──────────────────────────────────────────────────────────
  Obtuviste:   12,800 filas · 7 columnas
  Se esperaba: 12,000 filas · 7 columnas
──────────────────────────────────────────────────────────
  💡 Te quedaron 12,800 filas y se esperaban 12,000. Si te
     quedaron más, drop_duplicates() sin subset no los ve…
══════════════════════════════════════════════════════════
```

El mensaje de error **no es genérico**: nombra el error más probable dado lo
que te salió. Léelo completo antes de cambiar código.

### Es tolerante

No te va a marcar error por el orden de las columnas, el orden de las filas,
el índice o un decimal de más. Si tu resultado es correcto, pasa — aunque
hayas llegado por otro camino que el del instructor.

### Dos avisos

**Un ejercicio marca ❌ a propósito.** El 1.8 te va a decir que tu código está
bien pero que faltan filas. Es correcto: el problema son los datos, y el 1.9
lo resuelve. No te quedes reescribiendo el código.

**Dos ejercicios no se califican.** El 3.1 y el 3.4 son gráficos. Un gráfico
mal hecho se ve mal, así que se juzgan con los ojos.

---

## Las celdas 🤔 de interpretación

Algunas celdas te piden **escribir**, no programar:

> ¿Cuál de las dos versiones presentas al comité?

Son celdas de texto: doble clic para editar, `Shift+Enter` para dar formato.
No tienen respuesta única y no las califica nadie — son el punto del curso.
Un analista que sabe limpiar datos pero no sabe explicar qué significan no
sirve de mucho.

Escríbelas de verdad. Las vas a necesitar en el reto.

---

## Si te atoras o te atrasas 🛟

**No pasa nada, y no te vas a quedar fuera.**

Cada notebook arranca leyendo un archivo ya preparado de
`datos/checkpoints/`, no de lo que produjiste en el bloque anterior. Así que
si no terminaste el bloque 1, puedes abrir el bloque 2 y seguir con el grupo
sin ningún problema.

```
01 ──▶ 💾 hechos_limpios.parquet
                    │
                    ▼
02 ──▶ 💾 hechos_variance.parquet
                    │
                    ▼
03 ──▶ 📄 reporte_final_powerbi.csv
```

Los checkpoints ya vienen en el repositorio. Si tu bloque 1 no terminó, el
bloque 2 usa el checkpoint correcto de todas formas.

**Recomendación:** si un ejercicio te toma más de 4 minutos, avanza. Vuelves
al final si te queda tiempo.

---

## El reto final

`04_reto_final.ipynb` **no se hace al final**. Se abre en el minuto 65 y se
avanza por partes:

| Paso | Cuándo |
|---|---|
| 📍 1 | después del bloque 01 |
| 📍 2 | después del bloque 02 |
| 📍 3 | después del bloque 03 |
| 🏁 Entrega | al cierre |

Es **individual** y usa otro dataset. La última celda te da un código de
entrega que mandas junto con tu CSV.

---

## Atajos de teclado

| | |
|---|---|
| `Shift+Enter` | ejecutar la celda y pasar a la siguiente |
| `Ctrl+Enter` | ejecutar y quedarse en la celda |
| `Esc` `M` | convertir la celda en texto |
| `Esc` `Y` | convertir la celda en código |
| doble clic | editar una celda de texto |

Si algo se queda colgado: `Ctrl+Shift+P` → `Jupyter: Restart Kernel`. Ojo, eso
borra las variables y hay que volver a ejecutar desde arriba.
