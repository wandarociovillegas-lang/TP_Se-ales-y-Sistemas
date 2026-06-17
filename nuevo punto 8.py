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


################################# filtro antialiasing #################################

def filtro_pasabajos_ventana(fc, fs, orden):
    h = np.zeros(orden + 1) #lleno un array de ceros con el tamaño de cantidad de coeficientes = orden + 1
    wc = 2 * np.pi * fc / fs  #fc a wc discreta

    #coeficientes de Fourier ak del filtro ideal siendo una función sinc
    for n in range(orden + 1):
        k = n - orden/2

        if k == 0:
            h_ideal = wc/np.pi
        else:
            h_ideal = np.sin(wc*k)/(np.pi*k)

        #eligiendo ventanear con ventana de Hamming
        window_hamming = 0.54 - 0.46*np.cos(2*np.pi*n/orden)
        h[n] = h_ideal * window_hamming

    return h


def convolucion(x, h):
    y = np.zeros(len(x)) #lleno un array de ceros con el mismo tamaño que x

    for n in range(len(x)):
        suma = 0
        for k in range(len(h)):
            if n-k >= 0:
                suma += h[k]*x[n-k]
        y[n] = suma

    return y

def filtro_antialiasing(x, fc, fs, orden):
    h = filtro_pasabajos_ventana(fc, fs, orden)
    y = convolucion(x, h)

    return y

N = 2 #factor del decimador
fc = fs_entrada /(2 * N )  #frecuencia de corte
orden =  100 #calidad del filtro


signal_filtrada = filtro_antialiasing(signal_entrada, fc, fs_entrada, orden)


#################################     decimador       #################################
def decimador(x, n):
    return x[::n]

signal_salida = decimador(signal_filtrada, N)
fs_salida = fs_entrada


#################################   señal de salida   #################################

sf.write("audiolento_velocidadx2.wav", signal_salida, fs_salida) #mismo fs que la original para que sea el doble de la velocidad (lógica)


#################################   gráficos temporales  #################################
t_entrada = np.arange(len(signal_entrada)) /fs_entrada
t_salida = np.arange(len(signal_salida)) /fs_salida
t_rapido = np.arange(len(signal_rapida)) / fs_rapido

plt.figure(figsize=(12, 8))
plt.subplot(3, 1, 1)
plt.plot(t_entrada, signal_entrada)
plt.title("Señal de voz lenta")
plt.ylabel("Amplitud")
plt.xlabel("Tiempo [s]")
plt.grid()

plt.subplot(3, 1, 2)
plt.plot(t_entrada, signal_filtrada)
plt.title("Señal de voz lenta filtrada")
plt.ylabel("Amplitud")
plt.xlabel("Tiempo [s]")
plt.grid()

plt.subplot(3, 1, 3)
plt.plot(t_salida, signal_salida)
plt.title("Señal de voz lenta filtrada decimada")
plt.ylabel("Amplitud")
plt.xlabel("Tiempo [s]")
plt.grid()

plt.tight_layout(pad = 0.5)
plt.show()

plt.subplot(2, 1, 1)
plt.plot(t_salida, signal_salida)
plt.title("Señal de voz lenta filtrada decimada")
plt.ylabel("Amplitud")
plt.xlabel("Tiempo [s]")
plt.grid()


plt.subplot(2, 1, 2)
plt.plot(t_rapido, signal_rapida)
plt.title("Señal de voz rápida")
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

espectrograma_angosta_completo(signal_entrada, fs_entrada, int(20480), "original")
espectrograma_angosta_completo(signal_filtrada, fs_entrada, int(20480), "filtrada")
espectrograma_angosta_completo(signal_salida, fs_salida, int(20480),"salida")
espectrograma_angosta_completo(signal_rapida, fs_rapido, int(4096), "rápida") 

espectrograma_ancha_completo(signal_entrada, fs_entrada, int(1040), "original")
espectrograma_ancha_completo(signal_filtrada, fs_entrada, int(1040), "filtrada")
espectrograma_ancha_completo(signal_salida, fs_salida, int(768),"salida")
espectrograma_ancha_completo(signal_rapida, fs_rapido, int(512), "rápida")

