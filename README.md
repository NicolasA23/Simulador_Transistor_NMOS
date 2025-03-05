# Simulador de MOSFET Tipo N

La finalidad de este proyecto es desarrollar un simulador de transistores MOSFET, en este caso de tipo N, en Python. Este simulador permite calcular la corriente drain (ID) en función de la tensión de drain-source (VDS) y la tensión de gate-source (VGS). 

## Objetivo
El objetivo de este simulador es proporcionar una herramienta que permita visualizar el comportamiento de un MOSFET tipo N en función de parámetros físicos y eléctricos que el usuario puede ajustar.

## Requisitos
Este simulador utiliza las siguientes bibliotecas de Python:

```python
import numpy as np
import matplotlib.pyplot as plt
```

## Cómo usar el simulador
Ejecuta el script en Python para generar gráficas de la corriente drain (ID) contra el voltaje drain-source (VDS) para diferentes valores de VGS.

### Parámetros configurables
El usuario puede modificar los siguientes parámetros en el código:
- **dopaje_semiconductor (Na)**: Concentración de dopaje
- **temperatura (T)**: Temperatura del sistema
- **movilidad_electrones (mu0)**: Movilidad de los electrones en condiciones normales
- **ancho_canal (W)**: Ancho del canal del MOSFET
- **largo_canal (L)**: Largo del canal del MOSFET
- **espesor_oxido (tox)**: Espesor del óxido
- **funcion_trabajo_metal (Φm)** y **funcion_trabajo_semiconductor (Φs)**: Funciones de trabajo
- **carga_superficial (Qss)**: Carga superficial
- **factor_lambda (λ)**: Coeficiente de modulación del canal

## Explicación del Código
El código se divide en tres funciones principales:

### 1. Cálculo del coeficiente K
```python
def calcular_k(movilidad, temperatura, perm_vacio, perm_oxido, espesor_oxido):
    movilidad_ajustada = movilidad * (temperatura / 300) ** 2
    capacitancia_oxido = (perm_vacio * perm_oxido) / espesor_oxido
    return movilidad_ajustada * capacitancia_oxido
```
En esta función se calcula el coeficiente K en función de la movilidad de los electrones y la capacitancia del óxido. La función recibe 5 variables que son: movilidad, temperatura, permeabilidad en el vacío, permeabilidad del óxido y espesor del óxido.

### 2. Cálculo del voltaje de umbral (Vt)
```python
def calcular_vt(trabajo_metal, trabajo_semiconductor, carga_superficial, dopaje, concentracion_intrinseca, espesor_oxido, permitividad_oxido, permitividad_semiconductor):
    voltaje_termico = (1.38e-23 * temperatura) / 1.6e-19
    diferencia_trabajo = trabajo_metal - trabajo_semiconductor
    voltaje_banda_plana = diferencia_trabajo - (carga_superficial / (permitividad_oxido / espesor_oxido))
    potencial_fermi = voltaje_termico * np.log(dopaje / concentracion_intrinseca)
    carga_agotamiento = np.sqrt(2 * 1.6e-19 * permitividad_semiconductor * dopaje * 2 * potencial_fermi)
    capacitancia_oxido = permitividad_oxido / espesor_oxido
    voltaje_umbral = voltaje_banda_plana + 2 * potencial_fermi + (carga_agotamiento + carga_superficial) / capacitancia_oxido
    return voltaje_umbral
```
Esta función calcula el voltaje de umbral (Vt), que determina cuándo el MOSFET empieza a conducir.

### 3. Cálculo de la corriente drain (ID)
```python
def calcular_corriente(vgs, vds, coeficiente_k, ancho_canal, largo_canal, voltaje_umbral, factor_lambda):
    if vgs < voltaje_umbral:
        return 0  # Región de corte
    elif vgs > voltaje_umbral and vds < (vgs - voltaje_umbral):
        return coeficiente_k * (ancho_canal / largo_canal) * ((vgs - voltaje_umbral) * vds - (vds ** 2) / 2)  # Región lineal
    else:
        return 0.5 * coeficiente_k * (ancho_canal / largo_canal) * ((vgs - voltaje_umbral) ** 2) * (1 + factor_lambda * vds)  # Región de saturación
```
Esta función evalúa en qué región de operación se encuentra el MOSFET y calcula la corriente drain (ID) en función de VGS y VDS.

## Ejemplo de ejecución
Si ejecutamos el script con los valores por defecto, obtenemos la siguiente gráfica:

```python
valores_vds = np.linspace(0, 2, 100)
valores_vgs = [2, 3]  # Diferentes valores de VGS

plt.figure(figsize=(8, 6))
for vgs in valores_vgs:
    valores_id = [calcular_corriente(vgs, vds, coeficiente_k, ancho_canal, largo_canal, voltaje_umbral, factor_lambda) for vds in valores_vds]
    plt.plot(valores_vds, valores_id, label=f'VGS = {vgs} V')

plt.xlabel("VDS (V)")
plt.ylabel("ID (A)")
plt.title("Curva ID vs VDS para diferentes VGS (MOSFET Tipo N)")
plt.legend()
plt.grid()
plt.show()
```

Esto generará una gráfica que muestra la corriente drain en función del voltaje de drain-source para distintos valores de VGS.

