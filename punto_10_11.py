import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import soundfile as sf

audio_lento = "subir/audio_lento2_org.wav"

signal_x, fs = sf.read(audio_lento)

NFFT = int(4080)       


def decibeles(transformada):
    return 20 * np.log10(np.abs(transformada) + 1e-10)

def aumentar_velocidad(transformada, tiempo, tasa):
    transformada_nueva = []
    columnas_seleccionadas = []
    tiempo_nuevo =[]

    muestreo = int(tasa)

    for e in range(len(transformada[0])):
        if (e%muestreo == 0):
            columnas_seleccionadas.append(transformada[:,e])
            tiempo_nuevo.append(tiempo[e]/2)
        
    transformada_nueva = np.column_stack(columnas_seleccionadas)

    return transformada_nueva, tiempo_nuevo

def reducir_velocidad(transformada, tiempo, tasa):
    transformada_nueva = []
    columnas_seleccionadas = []
    tiempo_nuevo = []
    tiempo = tiempo*2
    muestreo = int(tasa)

    for e in range(len(transformada[0])):
        columnas_seleccionadas.append(transformada[:,e])
        columnas_seleccionadas.append(transformada[:,e])
        tiempo_nuevo.append(tiempo[e]/2)
        tiempo_nuevo.append(tiempo[e])

    transformada_nueva = np.column_stack(columnas_seleccionadas)

    return transformada_nueva, tiempo_nuevo

def construir_rapido(signal_x, NFFT, overlap, factor):
    noverlap = int(NFFT*overlap)
    frecuencias, tiempo, transformada = signal.stft(signal_x, fs=fs, nperseg=NFFT, noverlap=noverlap)
    transformada_nueva, tiempo_nuevo = aumentar_velocidad(transformada, tiempo, factor)
    t_signal, signal_y = signal.istft(transformada_nueva, fs=fs, nperseg=NFFT, noverlap=noverlap, window="hann")

    return t_signal, signal_y

def construir_lento(signal_x, NFFT, overlap, factor):
    noverlap = int(NFFT*overlap)
    frecuencias, tiempo, transformada = signal.stft(signal_x, fs=fs, nperseg=NFFT, noverlap=noverlap)
    transformada_nueva, tiempo_nuevo = reducir_velocidad(transformada, tiempo, factor)
    t_signal, signal_y = signal.istft(transformada_nueva, fs=fs, nperseg=NFFT, noverlap=noverlap, window="hann")

    return t_signal, signal_y


t_1, lento_0_5overlap = construir_lento(signal_x, NFFT, 0.5, 2)
t_2, lento_0_overlap = construir_lento(signal_x, NFFT, 0, 2)

t_3, rapido_0_5overlap = construir_rapido(signal_x, NFFT, 0.5, 2)
t_4, rapido_0_overlap = construir_rapido(signal_x, NFFT, 0, 2)


""" sf.write("lento_0_5overlap.wav", lento_0_5overlap, fs )
sf.write("lento_0overlap.wav", lento_0_overlap, fs)

sf.write("rapido_0_5overlap.wav", rapido_0_5overlap, fs)
sf.write("rapido_0overlap.wav", rapido_0_overlap, fs)
"""
#========= graficos ============#
audio_4 = "/home/marcos/UBA/sys_jupyter/lento_0_5overlap.wav"

signal_4, fs = sf.read(audio_4)

#fs 88200

overlap=0.95
NFFT= 20480
noverlap = int(NFFT*overlap)
figsize = (10, 6)
plt.figure(figsize=figsize)
plt.specgram(signal_4, Fs=fs, NFFT=NFFT, noverlap=noverlap, cmap='RdBu_r', vmin=-120, vmax=-60)
plt.ylim(0, 4000)
plt.colorbar(label='Intensidad (dB)')
plt.title('Espectrograma')
plt.xlabel('Tiempo (s)')
plt.ylabel('Frecuencia (Hz)')
plt.tight_layout()
plt.show()



plt.figure(figsize=figsize)
plt.specgram(lento_0_5overlap, Fs=fs, NFFT=NFFT, noverlap=noverlap, cmap='RdBu_r', vmin=-120, vmax=-60)
plt.ylim(0, 4000)
plt.colorbar(label='Intensidad (dB)')
plt.title('Espectrograma')
plt.xlabel('Tiempo (s)')
plt.ylabel('Frecuencia (Hz)')
plt.tight_layout()
plt.show()


