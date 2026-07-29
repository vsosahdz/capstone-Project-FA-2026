# Curso de cierre · Procesamiento de datos financieros con Python

Práctica guiada de 4 horas para el equipo de Finanzas y Contabilidad.

Recorres una vez, de principio a fin, el flujo real de trabajo de un analista:
recibes una petición ambigua de la Dirección de Finanzas, acondicionas datos
sucios, los analizas con SQL, construyes la narrativa visual y entregas un
archivo limpio para Power BI.

**Requisito previo:** los cursos introductorios de pandas + matplotlib +
DuckDB, y de Python con Power BI.

---

## Empezar

1. Sigue **[docs/01_INSTALACION.md](docs/01_INSTALACION.md)** (15–20 min).
2. Abre `notebooks/00_verificacion_entorno.ipynb` y ejecuta la única celda.
   Si todo sale ✅, ya está.
3. Sigue con `01_caso_e_ingesta.ipynb`.

Si te atoras en la instalación, avisa al instructor y **empieza igual**: cada
notebook arranca de un archivo ya preparado, así que puedes incorporarte en
cualquier bloque.

---

## Agenda

| | Bloque | Qué haces | Min |
|---|---|---|---|
| `00` | Setup | Entorno y verificación | 20 |
| `01` | Ingesta y limpieza | Los cinco problemas de los datos crudos | 45 |
| | 🎯 Reto · paso 1 | Individual | 5 |
| `02` | SQL con DuckDB | Filtrar, agrupar, combinar tres tablas | 35 |
| | 🎯 Reto · paso 2 | Individual | 5 |
| | ☕ Break | | 20 |
| `03` | Storytelling | Cuatro gráficos y la doble salida | 50 |
| | 🎯 Reto · paso 3 | Individual | 10 |
| `04` | Reto · entrega | Conclusión y código de entrega | 20 |
| | Cierre | | 10 |

Detalle completo en [docs/03_AGENDA.md](docs/03_AGENDA.md).

---

## El caso

> *"Necesito entender por qué el gasto de Hermosillo se disparó en el Q2.
> Quiero saber si es algo puntual o una tendencia, y qué centros de costo lo
> explican."*
> — Dirección de Finanzas

Análisis de desviación presupuestal sobre 4 plantas y 8 centros de costo, con
18 meses de historia. Los datos son **sintéticos**: ninguna cifra corresponde
a información real de la empresa.

---

## Qué hay en cada carpeta

```
notebooks/    los cinco notebooks del curso, en orden
docs/         instalación, cómo usar los notebooks, agenda
datos/
  crudos/     los CSV del caso, tal como llegan (sucios, a propósito)
  reto/       los CSV del reto final
  checkpoints/ archivos intermedios ya preparados 🛟
utils/        el módulo de autoverificación
salidas/      aquí escribes tus CSV
```

---

## Cómo funciona la autoverificación

Los ejercicios se califican solos:

```python
verificar("1.3", dim_cc)
```

```
  ✅  Ejercicio 1.3 correcto      8 filas · 3 columnas
```

Si te equivocas, te dice qué obtuviste, qué se esperaba y una pista concreta
del error más probable. No necesitas esperar al instructor.

Más detalle en [docs/02_COMO_USAR_NOTEBOOKS.md](docs/02_COMO_USAR_NOTEBOOKS.md).

> Las soluciones se publican en este mismo repositorio **al terminar el
> curso**.

---

## Qué NO cubre

* Construir el tablero dentro de Power BI. El curso termina en el CSV.
* Administración de bases de datos. Todo el SQL corre con DuckDB, sin
  servidor.
* Sintaxis nueva de pandas o matplotlib: aplicas lo que ya sabes a un flujo
  nuevo.
