import numpy as np
from matplotlib import pyplot as plt
from scipy import signal
import librosa
import soundfile as sf
archivo ="/home/marcos/UBA/sys_jupyter/tp2/lento2.wav"

signal_x ,fs = librosa.load(archivo, sr=None)
signal_y = signal_x.copy()



#========== ventanas ===========#
inicio_A1 = 1.06  ##1.32
final_A1 = 2.44   ##2.44

inicio_A2 = 2.84  ##3.02
final_A2 = 4.17   ##4.17

inicio_o = 4.68   ##4.94
final_o = 5.85    ##5.85

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
    dif = picos[0]
    lista.append(dif)
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
    print(int(total))
    return int(total)

def secuenciar(picos, inicio):
    secuencia = []
    for e in range(len(picos)):
        secuencia.append(picos[e]+inicio)
    return secuencia

periodo_medio_A1 = dif_promedio(picos_A1) # = 650.0666666666667
periodo_medio_A2 = dif_promedio(picos_A2) # = 643.624203821656
periodo_medio_o = dif_promedio(picos_o) # = 742.4766355140187

periodos_A1=dif_local(picos_A1)
periodos_A2=dif_local(picos_A2)
periodos_o=dif_local(picos_o)



# hasta aca consegui la distancia promedio entre los periodos, las distancias individuales entre los periodos, y la secuencia
# las secuencias tambien ubican los picos pero ahora desde la señal entera y no el segmento

#plt.plot(seg_A1[0:periodos_A1[0]+periodos_A1[1]+ periodos_A1[2]])
#plt.show()


#========= nueva señal ============#

def remover_segmento(indice_inicial, indice_final):
    signal_y[indice_inicial: indice_final] = np.zeros(indice_final-indice_inicial)

def sec_mas_cercana(numero, secuencia):
    return min(range(1, len(secuencia)-1), key=lambda x :abs(secuencia[x]-numero)) #pongo 1 para evitar pico en 0

def nuevos_picos(factor, periodo_prom, indice_inicial, indice_final):
    nuevo_periodo = int(periodo_prom*factor)
    puntero = indice_inicial 
    nuevos_t0= []
    while(puntero < indice_final):
        #signal_y[puntero] = 0.01              para probar donde estan los nuevos puntos
        nuevos_t0.append(puntero)
        puntero += nuevo_periodo
    return nuevos_t0
        
def psola(secuencia_vieja, periodos_viejos, nuevos_t0, signal_x, signal_y):
    #skipear primer pico viejo y nuevo
    for t in range(1,len(nuevos_t0)-1) : # recorro los t0 nuevos
        puntero = nuevos_t0[t]
        punto_seleccionado = sec_mas_cercana(puntero, secuencia_vieja) # me da el pico viejo mas cercano al nuevo
        

        ventana = signal_x[secuencia_vieja[punto_seleccionado-1]: secuencia_vieja[punto_seleccionado+1]]
        

        hann_v = signal.windows.hann(periodos_viejos[punto_seleccionado]+periodos_viejos[punto_seleccionado+1])
        prod = ventana * hann_v


        signal_y[nuevos_t0[t]-periodos_viejos[punto_seleccionado]:nuevos_t0[t]+periodos_viejos[punto_seleccionado+1]] += prod
    

remover_segmento(indice_inicio_A1, indice_final_A1)
remover_segmento(indice_inicio_A2, indice_final_A2)
remover_segmento(indice_inicio_O, indice_final_O)

secuencia_A1 = secuenciar(picos_A1, indice_inicio_A1)
secuencia_A2 = secuenciar(picos_A2, indice_inicio_A2)
secuencia_o = secuenciar(picos_o, indice_inicio_O)

efecto = 0.7 #cambiar periodo fundamental

t_A1_nuevo = nuevos_picos(efecto, periodo_medio_A1, indice_inicio_A1, indice_final_A1 )
t_A2_nuevo = nuevos_picos(efecto, periodo_medio_A2, indice_inicio_A2, indice_final_A2)
t_o_nuevo = nuevos_picos(efecto, periodo_medio_A2, indice_inicio_O, indice_final_O)

psola(secuencia_A1, periodos_A1, t_A1_nuevo, signal_x, signal_y)
psola(secuencia_A2, periodos_A2, t_A2_nuevo, signal_x, signal_y)
psola(secuencia_o, periodos_o, t_o_nuevo, signal_x, signal_y)

sf.write("sintetizacion_factor_0.7.wav", signal_y, fs)


#========= graficos =======#

t_signal_x = np.arange(len(signal_x)) / fs
t_signal_y = np.arange(len(signal_y)) / fs

t_A1 = np.arange(len(seg_A1)) / fs
t_A2 = np.arange(len(seg_A2)) / fs
t_o = np.arange(len(seg_o)) / fs

plt.subplot(2, 1, 1)
plt.plot(t_signal_x, signal_x)
plt.title("Señal original")

plt.ylabel("Amplitud")
plt.subplot(2, 1, 2)
plt.plot(t_signal_y, signal_y)
plt.title("Señal señal alterada")
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud")

plt.tight_layout()
plt.show()

plt.subplot(2,1 ,1)
plt.plot(t_signal_x[secuencia_A1[1]:secuencia_A1[5]],signal_x[secuencia_A1[1]:secuencia_A1[5]])
plt.title("Porcion de señal original")

plt.ylabel("Amplitud")
plt.subplot(2,1 ,2)
plt.plot(t_signal_y[secuencia_A1[1]:secuencia_A1[5]],signal_y[secuencia_A1[1]:secuencia_A1[5]])
plt.title("Misma porcion de la señal sintetizada")
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud")

plt.tight_layout()
plt.show()


    

plt.subplot(3, 1, 1)
plt.plot(t_A1, seg_A1)
plt.stem(t_A1[picos_A1], seg_A1[picos_A1],linefmt="red", markerfmt="x", basefmt="none")
plt.title("Señal de la vocal A1")

plt.ylabel("Amplitud")


plt.subplot(3, 1, 2)
plt.plot(t_A2, seg_A2)
plt.stem(t_A2[picos_A2], seg_A2[picos_A2], linefmt="red", markerfmt="x", basefmt="none")
plt.title("Señal de la vocal A2")

plt.ylabel("Amplitud")

plt.subplot(3, 1, 3)
plt.plot(t_o,seg_o)
plt.stem(t_o[picos_o], seg_o[picos_o], linefmt="red", markerfmt="x", basefmt="none" )
plt.title("Señal de la vocal O")
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud")

plt.tight_layout()
plt.show()


#test = seg_A1[picos_A1[0]:picos_A1[2]]
#hann_w = signal.windows.hann(periodos_A1[1]+periodos_A1[2])
#prod = test * hann_w

"""         plt.subplot(2,1,1)
        plt.plot(ventana)
        plt.title("Ejemplo de periodo unico de señal")
        plt.ylabel("Amplitud")
        plt.subplot(2,1,2)
        plt.plot(prod)
        plt.title("Ventaneo hann")
        plt.xlabel("Tiempo [s]")
        plt.ylabel("Amplitud")
        plt.tight_layout()
        plt.show() """
