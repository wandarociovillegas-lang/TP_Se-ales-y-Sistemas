import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.interpolate import PchipInterpolator
import librosa


a_rapido = "rapido.wav"
def_lento = "lento2.wav"

file = def_lento

data, fs = librosa.load(file, sr=None)

ts = 1/fs



#============ Ventana a graficar ===================#

inicio_A1 = 0.85
final_A1 = 1.58

inicio_A2 = 2.2
final_A2 = 2.6

inicio_o = 3.7
final_o = 4.2

inicio_S = 4.36
final_S = 5.14

#===================== periodos ====================#

t2_inicio_lenta = 2.815
t2_final_lenta = 2.823

t2_o_inicio_lenta =3.605
t2_o_final_lenta =3.614


ventana_inicio = inicio_o
ventana_final = final_o

sample_start = int(ventana_inicio*fs)
sample_end = int(ventana_final*fs)



window = data[sample_start:sample_end]

windowed_rfft =np.abs(np.fft.rfft(window))
rfft_frequencia = np.fft.rfftfreq(n=len(window),d=ts)

#==================================== funciones especiales ===============================================#

picos, propiedades = find_peaks(windowed_rfft, height=np.max(windowed_rfft)*0.05, distance=50, prominence=25 )

#distancia = 50
#prominencia = 25

idx = np.concatenate(([0], picos, [len(windowed_rfft) - 1]))
mag = windowed_rfft[idx]
envolvente = PchipInterpolator(idx, mag)(np.arange(len(windowed_rfft))).clip(0)


#============ Registro formates =============#

print("-------Picos--------")
for e in range(len(picos)):
    print("P"+ str(e), rfft_frequencia[picos[e]], windowed_rfft[picos[e]])


#======================== graficos ===================#

plt.subplot(2,1,1)
plt.title("Espectro de frecuencias O1")
plt.plot(data)
plt.grid()
plt.axvspan(sample_start, sample_end, color='orange', alpha=0.5, label='Ventana seleccionada')


plt.subplot(2,1,2)
plt.plot(rfft_frequencia, windowed_rfft)
plt.plot(rfft_frequencia, envolvente, color='red', linewidth=1)

plt.stem(rfft_frequencia[picos],windowed_rfft[picos], linefmt="red", markerfmt="x", basefmt="none")
plt.xlim(100, 2000)
plt.grid()
plt.ylabel("Modulo")
plt.xlabel("Frecuencia [Hz]")

plt.show()


