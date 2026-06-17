import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import firwin, lfilter
import soundfile as sf

audio_lento = "audio_lento.wav"
audio_rapido = "rapido.wav"

fs_entrada, x = wavfile.read(audio_lento)
signal_entrada = x / np.max(np.abs(x))

fs_rapido, x = wavfile.read(audio_rapido)
signal_rapida = x/ np.max(np.abs(x))



#################################   expansor   #################################
N = 2 #factor expanstor


def expansor(x, N):
    y = np.zeros(N * len(x)) #por defecto es una señal llena de ceros

    y[::N] = x  #intercalo por el factor expansor con valores de la señal x

    return y

signal_expandida = expansor(signal_rapida, N)
fs_expandida = fs_rapido * N #porque tengo el doble de muestras

#espectralmente se comprime el eje de frecuencia y se generan copias, las elimino con un interpolador 


#################################  interpolador  #################################

def interpolador_ideal(x, fs_rapido , N):
    orden = 100
    cant_coef = orden + 1

    fc = fs_rapido / (2 * N)

    h = firwin(cant_coef, cutoff = fc, fs = fs_rapido, window = "hamming")

    signal_interpolada = lfilter(h,1, x)
    signal_interpolada *= N  #ganancia del interpolador

    return signal_interpolada

signal_salida = interpolador_ideal(signal_expandida, fs_rapido, N)



#################################   señal de salida   #################################

fs_salida = fs_rapido
sf.write("audiorapido_velocidad_lenta.wav", signal_salida, fs_salida)


#################################   gráficos temporales  #################################

t_rapido = np.arange(len(signal_rapida)) / fs_rapido
t_expandida = np.arange(len(signal_expandida)) / fs_rapido
t_salida = np.arange(len(signal_salida)) /fs_salida

t_entrada = np.arange(len(signal_entrada)) /fs_entrada

plt.figure(figsize=(12, 8))
plt.subplot(3, 1, 1)
plt.plot(t_rapido, signal_rapida)
plt.title("Señal de voz rápida")
plt.ylabel("Amplitud")
plt.xlabel("Tiempo [s]")
plt.grid()


plt.subplot(3, 1, 2)
plt.plot(t_expandida, signal_expandida)
plt.title("Señal de voz rápida expandida")
plt.ylabel("Amplitud")
plt.xlabel("Tiempo [s]")
plt.grid()


plt.subplot(3, 1, 3)
plt.plot(t_salida, signal_salida)
plt.title("Señal de voz rápida expandida filtrada")
plt.ylabel("Amplitud")
plt.xlabel("Tiempo [s]")
plt.grid()

plt.tight_layout(pad = 0.5)
plt.show()

plt.subplot(2, 1, 1)
plt.plot(t_salida, signal_salida)
plt.title("Señal de voz rápida expandida filtrada")
plt.ylabel("Amplitud")
plt.xlabel("Tiempo [s]")
plt.grid()


plt.subplot(2, 1, 2)
plt.plot(t_entrada, signal_entrada)
plt.title("Señal de voz lenta")
plt.ylabel("Amplitud")
plt.xlabel("Tiempo [s]")
plt.grid()

plt.tight_layout(pad = 0.5)
plt.show()


#################################   espectrogramas  #################################

def espectrograma_angosta_completo(x, fs, NFFT, nombre):       
    overlap = 0.9     

    noverlap = int(NFFT*overlap)  
    figsize = (10, 6)
    plt.figure(figsize=figsize)
    plt.specgram(x, Fs=fs, NFFT=NFFT, noverlap=noverlap, cmap='RdBu_r', vmin=-110, vmax=-30)  
    plt.ylim(0, 4000)  
    plt.colorbar(label='Intensidad (dB)')
    plt.title(f'Espectrograma de banda angosta de la señal {nombre}')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Frecuencia (Hz)')
    plt.tight_layout()
    plt.show()


def espectrograma_ancha_completo(x, fs, NFFT,nombre):
    overlap = 0.9      

    noverlap = int(NFFT*overlap)  
    figsize = (10, 6)
    plt.figure(figsize=figsize)
    plt.specgram(x, Fs=fs, NFFT=NFFT, noverlap=noverlap, cmap='RdBu_r', vmin=-110, vmax=-30)  
    plt.ylim(0, 4000)  
    plt.colorbar(label='Intensidad (dB)')
    plt.title(f'Espectrograma de banda ancha de la señal {nombre}')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Frecuencia (Hz)')
    plt.tight_layout()
    plt.show()


espectrograma_angosta_completo(signal_rapida, fs_rapido, int(4096), "rápida") 
espectrograma_ancha_completo(signal_rapida, fs_rapido, int(512), "rápida")

espectrograma_angosta_completo(signal_expandida, fs_expandida, int(4096), "expandida")
espectrograma_ancha_completo(signal_expandida, fs_expandida, int(512), "expandida") 

espectrograma_angosta_completo(signal_salida, fs_salida, int(4096), "salida") 
espectrograma_ancha_completo(signal_salida, fs_salida, int(512), "salida") 

espectrograma_angosta_completo(signal_entrada, fs_entrada, int(20480), "lenta")
espectrograma_ancha_completo(signal_entrada, fs_entrada, int(1040), "lenta")



############################  datos útiles   ############################

print("Rapida:", len(signal_rapida)/fs_rapido)
print("Expandida:", len(signal_expandida)/fs_rapido)
print("Salida:", len(signal_salida)/fs_salida)
print("Lenta:", len(signal_entrada)/fs_entrada)
