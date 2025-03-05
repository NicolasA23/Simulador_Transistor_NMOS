import matplotlib.pyplot as plt

def calcular_k(movilidad, temperatura, perm_vacio, perm_oxido, espesor_oxido):
    movilidad_ajustada = movilidad * (temperatura / 300) ** 2
    capacitancia_oxido = (perm_vacio * perm_oxido) / espesor_oxido
    return movilidad_ajustada * capacitancia_oxido

def calcular_vt(trabajo_metal, trabajo_semiconductor, carga_superficial, dopaje, concentracion_intrinseca, espesor_oxido, permitividad_oxido, permitividad_semiconductor, q=1.6e-19, k=1.38e-23, temperatura=300):
    voltaje_termico = (k * temperatura) / q
    diferencia_trabajo = trabajo_metal - trabajo_semiconductor
    voltaje_banda_plana = diferencia_trabajo - (carga_superficial / (permitividad_oxido / espesor_oxido))
    potencial_fermi = voltaje_termico * np.log(dopaje / concentracion_intrinseca)
    carga_agotamiento = np.sqrt(2 * q * permitividad_semiconductor * dopaje * 2 * potencial_fermi)
    capacitancia_oxido = permitividad_oxido / espesor_oxido
    voltaje_umbral = voltaje_banda_plana + 2 * potencial_fermi + (carga_agotamiento + carga_superficial) / capacitancia_oxido
    return voltaje_umbral

def calcular_corriente(vgs, vds, coeficiente_k, ancho_canal, largo_canal, voltaje_umbral, factor_lambda):
    if vgs < voltaje_umbral:
        return 0  # Región de corte
    elif vgs > voltaje_umbral and vds < (vgs - voltaje_umbral):
        return coeficiente_k * (ancho_canal / largo_canal) * ((vgs - voltaje_umbral) * vds - (vds ** 2) / 2)  # Región lineal
    else:
        return 0.5 * coeficiente_k * (ancho_canal / largo_canal) * ((vgs - voltaje_umbral) ** 2) * (1 + factor_lambda * vds)  # Región de saturación

# Parámetros físicos
permitividad_vacio = 8.85e-12  # F/m
permitividad_oxido = 3.9  # Relativa
movilidad_electrones = 600e-4  # m^2/Vs
temperatura = 298.15  # K

# Parámetros del MOSFET
ancho_canal = 10e-6  # m
largo_canal = 1e-6  # m
factor_lambda = 0.02  # Modulación de canal

# Parámetros para el cálculo de Vt
funcion_trabajo_metal = 4.1  # V
funcion_trabajo_semiconductor = 4.05  # V
carga_superficial = 1e-8  # C/m^2
dopaje_semiconductor = 1e22  # m^-3
concentracion_intrinseca = 1.5e16  # m^-3
espesor_oxido = 5e-9  # m
permitividad_oxido_fisica = permitividad_vacio * permitividad_oxido  # F/m
permitividad_semiconductor = 1.05e-10  # F/m

# Cálculo de coeficiente k y voltaje de umbral
coeficiente_k = calcular_k(movilidad_electrones, temperatura, permitividad_vacio, permitividad_oxido, espesor_oxido)
voltaje_umbral = calcular_vt(funcion_trabajo_metal, funcion_trabajo_semiconductor, carga_superficial, dopaje_semiconductor, concentracion_intrinseca, espesor_oxido, permitividad_oxido_fisica, permitividad_semiconductor)

# Rango de voltajes
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
