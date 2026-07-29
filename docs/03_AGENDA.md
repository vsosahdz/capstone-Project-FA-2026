# Agenda detallada

4 horas = **240 minutos**, de los cuales 20 son de break: **220 minutos
efectivos**.

```
 min │
   0 ├─ 00 · SETUP                                20  ████
     │       venv · requirements · kernel · verificación
  20 ├─ 01 · INGESTA Y LIMPIEZA                   45  █████████
     │       codificación · importes · duplicados · join roto
  65 ├─   🎯 RETO paso 1 · cargar y limpiar        5  █
  70 ├─ 02 · SQL CON DUCKDB                       35  ███████
     │       filtrar · agrupar · combinar 3 tablas · desviación
 105 ├─   🎯 RETO paso 2 · tu desviación           5  █
 110 ├─ ☕ BREAK                                   20
 130 ├─ 03 · STORYTELLING Y DOBLE SALIDA          50  ██████████
     │       4 gráficos · v1 vs v2 · exportar para Power BI
 180 ├─   🎯 RETO paso 3 · tu gráfico             10  ██
 190 ├─ 04 · RETO · conclusión y entrega          20  ████
 210 ├─ CIERRE                                    10  ██
 220 ┴
```

---

## Bloque 01 · Ingesta y limpieza · 45 min

Los cinco problemas de los datos crudos, cada uno con un síntoma distinto:

| | Problema | Cómo se nota | Ejercicio |
|---|---|---|---|
| ① | Archivo en otra codificación | truena al abrir | 1.3 |
| ② | Importes como texto | `.info()` dice `str` | 1.5 |
| ③ | 800 asientos duplicados | folios repetidos | 1.7 |
| ④ | Llaves de texto sucias | el join pierde 2,400 filas | 1.8 → 1.9 |
| ⑤ | Importes negativos | no es un error | 1.10 |

**Ejercicios:** 6 turnos (1.2, 1.3, 1.5, 1.7, 1.8, 1.9) + 1 celda de
interpretación.
**Salida:** `datos/checkpoints/hechos_limpios.parquet`

> 🛟 Válvula de escape: si el bloque va retrasado, el **1.5 pasa a
> demostración** del instructor.

---

## Bloque 02 · SQL con DuckDB · 35 min

De 12,000 asientos a una tabla de desviación de 576 filas.

**Ejercicios:** 4 turnos (2.2, 2.4, 2.6, 2.7).
**Salida:** `datos/checkpoints/hechos_variance.parquet`

Incluye la tabla de traducción pandas ↔ SQL, que conecta los dos cursos
previos.

> 🛟 Válvula de escape: el **2.4 pasa a demostración**.

---

## Bloque 03 · Storytelling y doble salida · 50 min

Cuatro gráficos, cada uno responde una frase del correo del directivo:

| Gráfico | Pregunta |
|---|---|
| 1 · Desviación por planta | ¿Cuánto? |
| 2 · Evolución mensual | ¿Cuándo empezó? |
| 3 · Top centros de costo | ¿Dónde está? |
| 4 · v1 contra v2 | ¿Puedo confiar en el dato? |

**Ejercicios:** 5 turnos (3.1, 3.4, 3.6, 3.9, 3.11) — de los cuales 3.1 y 3.4
son visuales y no se autocalifican — y 4 celdas de interpretación.
**Salida:** `salidas/reporte_final_powerbi.csv`

El clímax es el **3.10**: la misma consulta sobre datos crudos da $4.0M en
Hermosillo, y sobre datos limpios $1.0M — y resulta que Chihuahua está peor.
Es una conclusión distinta sobre una planta distinta.

> 🛟 Válvula de escape: el **3.9 pasa a demostración**.

---

## Bloque 04 · Reto final · 40 min repartidos

Individual, con otro dataset y otra pregunta. Se avanza intercalado:

| Paso | Cuándo | Min |
|---|---|---|
| 📍 1 · cargar y limpiar | tras el bloque 01 | 5 |
| 📍 2 · desviación | tras el bloque 02 | 5 |
| 📍 3 · gráfico e insight | tras el bloque 03 | 10 |
| 🏁 conclusión y entrega | al cierre | 20 |

La lección se invierte:

```
   CASO PRINCIPAL              RETO
   duplicados en HECHOS        duplicados en PRESUPUESTO
   parecía $4.0M               parecía $0.5M de ahorro
        ↓ limpiar                   ↓ limpiar
   eran $1.0M                  eran $2.0M de sobregasto
   el problema se ENCOGE       el problema APARECE
```

---

## Resumen de ejercicios

```
Notebook 01    6 turnos · 6 verificables  + 1 celda de interpretación
Notebook 02    4 turnos · 4 verificables
Notebook 03    5 turnos · 3 verificables  + 4 celdas de interpretación
Reto           4 pasos  · 4 verificables  + 1 conclusión
───────────────────────────────────────────────────────────────────────
19 turnos · 17 autocalificables · 6 celdas abiertas
4 gráficos · 3 válvulas de escape · 4 checkpoints
```
