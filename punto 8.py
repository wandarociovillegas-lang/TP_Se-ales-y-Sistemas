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


N = 2 #escala del decimador

################################# filtro antialiasing #################################
fc = fs_entrada /(2 * N )  #frecuencia de corte
orden =  4 #calidad del filtro


def aplicar_filtro_pasabajos(signal_entrada, fc, fs_entrada):
    
    cant_coef = 101  # longitud del filtro FIR
    h = firwin(cant_coef, cutoff=fc, fs=fs_entrada, window="hamming")
    signal_filtrada = lfilter(h, 1, signal_entrada)

    return signal_filtrada



signal_filtrada = aplicar_filtro_pasabajos(signal_entrada, fc, fs_entrada)


#################################     decimador       #################################

def decimador(x, n):
    return x[::n]

signal_salida = decimador(signal_filtrada, N)
fs_salida = fs_entrada


#################################   señal de salida   #################################

sf.write("audiolento_velocidadx2.wav", signal_salida, fs_salida) #mismo fs que la original para que sea el doble de la velocidad (lógica)




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
espectrograma_ancha_completo(signal_salida, fs_salida, int(768),"salida")
espectrograma_angosta_completo(signal_rapida, fs_rapido, int(4096), "rápida") 
espectrograma_ancha_completo(signal_rapida, fs_rapido, int(512), "rápida")