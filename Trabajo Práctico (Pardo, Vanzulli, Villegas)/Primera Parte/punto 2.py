import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

audio_lento = "lento2.wav"
audio_rapido = "rapido.wav"

fs_lento, x_lento = wavfile.read(audio_lento)
fs_rapido, x_rapido = wavfile.read(audio_rapido)

x_lento = x_lento / np.max(np.abs(x_lento)) 
t_lento = np.arange(len(x_lento)) / fs_lento


x_rapido = x_rapido / np.max(np.abs(x_rapido)) 
t_rapido = np.arange(len(x_rapido)) / fs_rapido

#ubico la A y la S a ojo en la señal lenta
inicio_A1 = 0.85
final_A1 = 1.58

inicio_A2 = 2.2
final_A2 = 2.9

inicio_o = 3.52
final_o = 4.25

inicio_S = 4.36
final_S = 5.14

#accedo e indexo a los tiempos de muestras 
indice_inicio_A1 = int(inicio_A1 * fs_lento)
indice_final_A1 = int(final_A1 * fs_lento)

indice_inicio_A2 = int(inicio_A2 * fs_lento)
indice_final_A2 = int(final_A2 * fs_lento)

indice_inicio_S = int(inicio_S * fs_lento)
indice_final_S = int(final_S * fs_lento)


#creo segmentos
seg_A1_lento = x_lento[indice_inicio_A1 : indice_final_A1]
seg_A2_lento = x_lento[indice_inicio_A2 : indice_final_A2]
seg_S_lento = x_lento[indice_inicio_S : indice_final_S]


t_A1_lento = t_lento[indice_inicio_A1 : indice_final_A1]
t_A2_lento = t_lento[indice_inicio_A2 : indice_final_A2]
t_S_lento = t_lento[indice_inicio_S : indice_final_S]


#graficoooooooo
plt.plot(t_lento, x_lento, linewidth= 0.8)
plt.ylabel("Amplitud", fontsize= 15.0)
plt.xlabel("Tiempo", fontsize= 15.0)
plt.title("Señal de voz lenta", fontsize= 20.0)
plt.show()

plt.plot(t_rapido, x_rapido, linewidth= 0.8)
plt.ylabel("Amplitud", fontsize= 15.0)
plt.xlabel("Tiempo", fontsize= 15.0)
plt.title("Señal de voz rápida", fontsize= 20.0)
plt.show()



plt.plot(t_A1_lento, seg_A1_lento, linewidth= 0.8)
plt.ylabel("Amplitud", fontsize= 15.0)
plt.xlabel("Tiempo", fontsize= 15.0)
plt.title("Señal cuasi-periodica de A1", fontsize= 20.0)
ax = plt.gca() #esto es para molestar básicamente hace que la amplitud se mantenga entre 1 y -1 sirve si lo querés comparar mejor
ax.set_ylim(-1.1, 1.1)
plt.show()

plt.plot(t_A2_lento, seg_A2_lento, linewidth= 0.8)
plt.ylabel("Amplitud", fontsize= 15.0)
plt.xlabel("Tiempo", fontsize= 15.0)
plt.title("Señal cuasi-periodica de A2", fontsize= 20.0)
ax = plt.gca() 
ax.set_ylim(-1.1, 1.1)
plt.show()

plt.plot(t_S_lento, seg_S_lento, linewidth= 0.8)
plt.ylabel("Amplitud", fontsize= 15.0)
plt.xlabel("Tiempo", fontsize= 15.0)
plt.title("Señal de S", fontsize= 20.0)
ax = plt.gca() 
ax.set_ylim(-1.1, 1.1)
plt.show()

#periodo y frecuencia en lenta
#se toman 5 muestras de la A2
t1_inicio_lenta = 2.807
t1_final_lenta = 2.815

t2_inicio_lenta = 2.815
t2_final_lenta = 2.823

t3_inicio_lenta = 2.823
t3_final_lenta = 2.831

t4_inicio_lenta = 2.831
t4_final_lenta = 2.839

t5_inicio_lenta = 2.538
t5_final_lenta = 2.546



t1_lenta = t1_final_lenta - t1_inicio_lenta
t2_lenta = t2_final_lenta - t2_inicio_lenta
t3_lenta = t3_final_lenta - t3_inicio_lenta
t4_lenta = t4_final_lenta - t4_inicio_lenta
t5_lenta = t5_final_lenta - t5_inicio_lenta

promedio_periodo_lenta = (t1_lenta + t2_lenta + t3_lenta + t4_lenta + t5_lenta) /5
print(f"Analisis de la lenta")
print(f"Periodo estimado en tiempo: {promedio_periodo_lenta} \nFrecuencia estimada: {1/promedio_periodo_lenta}")


#periodo y frecuencia en rápida
#4 muestras A1 es lo que alcanzo
t1_inicio_rapida = 0.698
t1_final_rapida = 0.711

t2_inicio_rapida = 0.723
t2_final_rapida = 0.736

t3_inicio_rapida = 0.749
t3_final_rapida = 0.761

t4_inicio_rapida = 0.775
t4_final_rapida = 0.787

t1_rapida = t1_final_rapida - t1_inicio_rapida
t2_rapida = t2_final_rapida - t2_inicio_rapida
t3_rapida = t3_final_rapida - t3_inicio_rapida
t4_rapida = t4_final_rapida - t4_inicio_rapida

promedio_periodo_rapida = (t1_rapida + t2_rapida + t3_rapida + t4_rapida) / 4
print(f"Analisis de la rápida")
print(f"Periodo estimado en tiempo: {promedio_periodo_rapida} \nFrecuencia estimada: {1/promedio_periodo_rapida}")


#señal de la o 
t1_o_inicio_lenta = 3.588
t1_o_final_lenta = 3.596

t2_o_inicio_lenta =3.605
t2_o_final_lenta =3.614

t3_o_inicio_lenta = 3.623
t3_o_final_lenta = 3.632

t4_o_inicio_lenta =3.641
t4_o_final_lenta =3.650

t5_o_inicio_lenta = 3.659
t5_o_final_lenta = 3.669

t1_o_lenta = t1_o_final_lenta - t1_o_inicio_lenta
t2_o_lenta = t2_o_final_lenta - t2_o_inicio_lenta
t3_o_lenta = t3_o_final_lenta - t3_o_inicio_lenta
t4_o_lenta = t4_o_final_lenta - t4_o_inicio_lenta
t5_o_lenta = t5_o_final_lenta - t5_o_inicio_lenta

promedio_periodo_o_lenta = (t1_o_lenta + t2_o_lenta + t3_o_lenta + t4_o_lenta+ t5_o_lenta) / 5
print(f"Analisis de la O lenta")
print(f"Periodo estimado en tiempo: {promedio_periodo_o_lenta} \nFrecuencia estimada: {1/promedio_periodo_o_lenta}")


t1_o_inicio_rapida = 1.201
t1_o_final_rapida = 1.208

t2_o_inicio_rapida = 1.214
t2_o_final_rapida = 1.220

t3_o_inicio_rapida = 1.227
t3_o_final_rapida = 1.234

t4_o_inicio_rapida = 1.240
t4_o_final_rapida = 1.247

t5_o_inicio_rapida = 1.254
t5_o_final_rapida = 1.261

t1_o_rapida = t1_o_final_rapida - t1_o_inicio_rapida
t2_o_rapida = t2_o_final_rapida - t2_o_inicio_rapida
t3_o_rapida = t3_o_final_rapida - t3_o_inicio_rapida
t4_o_rapida = t4_o_final_rapida - t4_o_inicio_rapida
t5_o_rapida = t5_o_final_rapida - t5_o_inicio_rapida

promedio_periodo_o_rapida = (t1_o_rapida + t2_o_rapida + t3_o_rapida + t4_o_rapida + t5_o_rapida) / 5
print(f"Analisis de la O rápida")
print(f"Periodo estimado en tiempo: {promedio_periodo_o_rapida} \nFrecuencia estimada: {1/promedio_periodo_o_rapida}")
