# Preguntas frecuentes — Datos meteorológicos de Madrid

Información sobre las **mediciones horarias** publicadas por el Ayuntamiento de Madrid en [datos.madrid.es](https://datos.madrid.es).

## ¿De dónde salen estos datos?

Provienen de la **red meteorológica municipal**, integrada en el Sistema Integral de la Calidad del Aire de Madrid. Las estaciones registran parámetros como temperatura, viento o humedad **cada hora**.

## ¿Qué mide cada código de magnitud?

En el fichero CSV, la columna **magnitud** indica qué parámetro se ha medido:

| Código | Parámetro | Unidad habitual |
|--------|-----------|-----------------|
| **81** | Velocidad del viento | m/s |
| **82** | Dirección del viento | grados (0–360) |
| **83** | Temperatura | °C |
| **86** | Humedad relativa | % |
| **87** | Presión barométrica | mb (hectopascales) |
| **88** | Radiación solar | W/m² |
| **89** | Precipitación | l/m² |

Cada fila del CSV corresponde a **un parámetro concreto** en una estación, para un día determinado.

## ¿Cómo se leen las columnas h01, h02… h24?

- **h01** → medición de la **1:00** (madrugada)
- **h12** → medición del **mediodía**
- **h24** → medición de las **24:00** (final del día)

Entre **h01** y **h24** hay un valor por cada hora del día, en **hora local de Madrid**.

Las columnas **v01…v24** indican si esa hora es fiable:

| Código | Significado |
|--------|-------------|
| **V** | Medición validada |
| **N** | Medición no válida |
| **T** | Provisional, pendiente de revisión técnica |

## ¿Qué es el punto de muestreo?

Es el identificador del sensor, por ejemplo `28102001_83_89`. Incluye la estación y la magnitud medida. Sirve para saber exactamente de qué aparato proviene cada fila.

## ¿Qué significan provincia, municipio y estación?

Son **códigos numéricos** de ubicación administrativa y de la red de medición. Permiten filtrar datos por zona sin depender del nombre textual del barrio.

## ¿Por qué hay varias filas el mismo día?

Porque la misma estación publica **una fila por magnitud**: temperatura, viento, humedad, etc. No es un error del fichero.

## ¿El CSV usa coma o punto decimal?

En este dataset los decimales van con **coma** (`4,6` = 4,6 °C) y las columnas se separan con **punto y coma** (`;`).

## ¿Para qué sirve el PDF del dataset?

Documenta la **estructura oficial del fichero**: nombre de columnas, códigos y advertencias. Las mediciones numéricas están en el CSV.

## Más información

- Portal: [datos.madrid.es](https://datos.madrid.es) — categoría *Medio ambiente*
- Mapa de la red: web de calidad del aire de Madrid
- Licencia: Creative Commons Attribution 4.0 (Ayuntamiento de Madrid)
