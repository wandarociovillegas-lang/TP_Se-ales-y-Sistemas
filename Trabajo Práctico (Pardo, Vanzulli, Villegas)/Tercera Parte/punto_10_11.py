import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import soundfile as sf

audio_lento = "subir/audio_lento2_org.wav"

signal_x, fs = sf.read(audio_lento)

NFFT = int(4080)       


def decibeles(transformada):
    return 20 * np.log10(np.abs(transformada) + 1e-10)

def aumentar_velocidad(transformada, tasa):
    transformada_nueva = []
    columnas_seleccionadas = []

    muestreo = int(tasa)

    for e in range(len(transformada[0])):
        if (e%muestreo == 0):
            columnas_seleccionadas.append(transformada[:,e])

        
    transformada_nueva = np.column_stack(columnas_seleccionadas)

    return transformada_nueva

def reducir_velocidad(transformada, tasa):
    transformada_nueva = []
    columnas_seleccionadas = []

    for e in range(len(transformada[0])):
        columnas_seleccionadas.append(transformada[:,e])
        columnas_seleccionadas.append(transformada[:,e])

    transformada_nueva = np.column_stack(columnas_seleccionadas)

    return transformada_nueva

def construir_rapido(signal_x, NFFT, overlap, factor):
    noverlap = int(NFFT*overlap)
    frecuencias, tiempo, transformada = signal.stft(signal_x, fs=fs, nperseg=NFFT, noverlap=noverlap)
    transformada_nueva = aumentar_velocidad(transformada, factor)
    t_signal, signal_y = signal.istft(transformada_nueva, fs=fs, nperseg=NFFT, noverlap=noverlap, window="hann")

    return signal_y

def construir_lento(signal_x, NFFT, overlap, factor):
    noverlap = int(NFFT*overlap)
    frecuencias, tiempo, transformada = signal.stft(signal_x, fs=fs, nperseg=NFFT, noverlap=noverlap)
    transformada_nueva = reducir_velocidad(transformada, factor)
    t_signal, signal_y = signal.istft(transformada_nueva, fs=fs, nperseg=NFFT, noverlap=noverlap, window="hann")

    return signal_y


lento_0_5overlap = construir_lento(signal_x, NFFT, 0.5, 2)
lento_0_overlap = construir_lento(signal_x, NFFT, 0, 2)

rapido_0_5overlap = construir_rapido(signal_x, NFFT, 0.5, 2)
rapido_0_overlap = construir_rapido(signal_x, NFFT, 0, 2)


sf.write("lento_tfct_0_5overlap.wav", lento_0_5overlap, fs )
sf.write("lento_tfct_0overlap.wav", lento_0_overlap, fs)

sf.write("rapido_tfct_0_5overlap.wav", rapido_0_5overlap, fs)
sf.write("rapido_tfct_0overlap.wav", rapido_0_overlap, fs)

#========= graficos ============#


""" overlap=0.95
NFFT= 20480
noverlap = int(NFFT*overlap)
figsize = (10, 6)
plt.figure(figsize=figsize)
plt.specgram(, Fs=fs, NFFT=NFFT, noverlap=noverlap, cmap='RdBu_r', vmin=-120, vmax=-60)
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
 """

