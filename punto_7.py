import numpy as np
from matplotlib import pyplot as plt
from scipy import signal
from scipy.io import wavfile

audio_lento = "audiolento.wav"

fs, signal_x = wavfile.read(audio_lento)
signal_x = signal_x / np.max(np.abs(signal_x ))
signal_y = []


#========== ventanas ===========#
inicio_A1 = 1.32
final_A1 = 2.44#-1

inicio_A2 = 3.02
final_A2 = 4.17#-1

inicio_o = 4.94
final_o = 5.85#-0.8

indice_inicio_A1 = int(inicio_A1 * fs)
indice_final_A1 = int(final_A1 * fs )

indice_inicio_A2 = int(inicio_A2 * fs)
indice_final_A2 = int(final_A2 * fs)

indice_inicio_O = int(inicio_o * fs)
indice_final_O = int(final_o * fs)

seg_A1 = signal_x[indice_inicio_A1 : indice_final_A1]
seg_A2 = signal_x[indice_inicio_A2 : indice_final_A2]
seg_o = signal_x[indice_inicio_O : indice_final_O]

#========== encontrar picos===========#

picos_A1, props_A1 = signal.find_peaks(-1*seg_A1, height= 0.007, distance=500 )
picos_A2, props_A2 = signal.find_peaks(-1*seg_A2, height=0.0049, distance=500)
picos_o, props_o = signal.find_peaks(-1*seg_o, height= 0.0040, distance=600)

#==== periodo promedio, intervalos y secuencias ======#

def dif_local(picos):
    lista = []
    for e in range(len(picos)-1) :
        dif=picos[e+1]-picos[e]
        lista.append(dif)
    return lista


def dif_promedio(picos):
    total = 0
    for e in range(len(picos)-1) :
        dif=picos[e+1]-picos[e]
        total += dif
        
    total /= len(picos)-1
    print(total)
    return total

def secuenciar(picos, inicio):
    secuencia = [inicio]
    for e in range(len(picos)):
        secuencia.append(picos[e]+inicio)
    return secuencia

#periodo en muestras
periodo_medio_A1 = dif_promedio(picos_A1) # = 650.0666666666667
periodo_medio_A2 = dif_promedio(picos_A2) # = 643.624203821656
periodo_medio_o = dif_promedio(picos_o) # = 742.4766355140187

periodos_A1 = dif_local(picos_A1)
periodos_A2 = dif_local(picos_A2)
periodos_o = dif_local(picos_o)


#periodos y frecuencias fundamentales de las vocales
T_A1 = periodo_medio_A1/fs
f0_A1 = 1/T_A1

T_A2 = periodo_medio_A2/fs
f0_A2 = 1/T_A2

T_0 = periodo_medio_o/fs
f0_o = 1/T_0



# hasta aca consegui la distancia promedio entre los periodos, las distancias individuales entre los periodos, y la secuencia
# las secuencias tambien ubican los picos pero ahora desde la señal entera y no el segmento

#plt.plot(seg_A1[0:periodos_A1[0]+periodos_A1[1]+ periodos_A1[2]])
#plt.show()

#========= nueva señal ============#
signal_y = signal_x.copy()
print(signal_y)

def remover_segmento(indice_inicial, indice_final):
    signal_y[indice_inicial: indice_final] = np.zeros(indice_final-indice_inicial)

remover_segmento(indice_inicio_A1, indice_final_A1)
remover_segmento(indice_inicio_A2, indice_final_A2)
remover_segmento(indice_inicio_O, indice_final_O)

plt.subplot(2, 1, 1)
plt.plot(signal_x)
plt.xlabel("Muestras")
plt.ylabel("Amplitud")
plt.title("Señal original")

plt.subplot(2, 1, 2)
plt.plot(signal_y)
plt.xlabel("Muestras")
plt.ylabel("Amplitud")
plt.title("Señal modificada")

plt.tight_layout()
plt.show()

#========= ventaneo =======#

""" def ventaneo_hann(periodos, picos, signal_x ):
    ventanas_hann = []
    for e in range(len(periodos)-1):
        ventanas_hann.append(signal.windows.hann(periodos[e]+periodos[e+1]))
    for e in range(len(periodos)-1):
        print("longitud",len(signal_x[picos[e]-periodos[e]:picos[e]+periodos[e+1]]))

        signal_y = signal_x[picos[e]-periodos[e]:picos[e]+periodos[e+1]] * ventanas_hann[e]
    return signal_y """



    
#========= graficar =======#

plt.subplot(3, 1, 1)
plt.plot(seg_A1)
plt.stem(picos_A1, seg_A1[picos_A1],linefmt="red", markerfmt="x", basefmt="none")
plt.title("Señal de la vocal A1")
plt.xlabel("Muestras")
plt.ylabel("Amplitud")

plt.subplot(3, 1, 2)
plt.plot(seg_A2)
plt.stem(picos_A2, seg_A2[picos_A2], linefmt="red", markerfmt="x", basefmt="none")
plt.title("Señal de la vocal A2")
plt.xlabel("Muestras")
plt.ylabel("Amplitud")

plt.subplot(3, 1, 3)
plt.plot(seg_o)
plt.stem(picos_o, seg_o[picos_o], linefmt="red", markerfmt="x", basefmt="none" )
plt.title("Señal de la vocal A2")
plt.xlabel("Muestras")
plt.ylabel("Amplitud")

plt.tight_layout()
plt.show()
