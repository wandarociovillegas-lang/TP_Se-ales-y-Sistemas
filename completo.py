import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

fs, x = wavfile.read("lento2.wav")
x = x / np.max(np.abs(x))

#punto 1
def espectrograma_angosta_completo(x, fs):
    NFFT = int(20480)       
    overlap = 0.9     

    noverlap = int(NFFT*overlap)  
    figsize = (10, 6)
    plt.figure(figsize=figsize)
    plt.specgram(x, Fs=fs, NFFT=NFFT, noverlap=noverlap, cmap='RdBu_r', vmin=-110, vmax=-30)  
    plt.ylim(0, 800)  
    plt.colorbar(label='Intensidad (dB)')
    plt.title('Espectrograma de banda angosta de toda la palabra')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Frecuencia (Hz)')
    plt.tight_layout()
    plt.show()

#punto 2
def espectrograma_ancha_completo(x, fs):
    NFFT = int(512)       
    overlap = 0.9      

    noverlap = int(NFFT*overlap)  
    figsize = (10, 6)
    plt.figure(figsize=figsize)
    plt.specgram(x, Fs=fs, NFFT=NFFT, noverlap=noverlap, cmap='RdBu_r', vmin=-110, vmax=-30)  
    plt.ylim(0, 4000)  
    plt.colorbar(label='Intensidad (dB)')
    plt.title('Espectrograma de banda ancha de toda la palabra')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Frecuencia (Hz)')
    plt.tight_layout()
    plt.show()

#punto 3
inicio_A1 = 0.85
final_A1 = 1.58

inicio_A2 = 2.2
final_A2 = 2.9

inicio_o = 3.52
final_o = 4.25

indice_inicio_A1 = int(inicio_A1 * fs)
indice_final_A1 = int(final_A1 * fs)

indice_inicio_A2 = int(inicio_A2 * fs)
indice_final_A2 = int(final_A2 * fs)

indice_inicio_O = int(inicio_o * fs)
indice_final_O = int(final_o * fs)

seg_A1 = x[indice_inicio_A1 : indice_final_A1]
seg_A2 = x[indice_inicio_A2 : indice_final_A2]
seg_o = x[indice_inicio_O : indice_final_O]

def espectrograma_angosta(seg, fs, nombre):

    NFFT = min(4080, len(seg)//2)
    overlap = 0.95 #aumento el solapamiento para mejor calidad de imagen

    noverlap = int(NFFT*overlap)  

    figsize = (10, 6)
    plt.figure(figsize=figsize)
    plt.specgram(seg, Fs=fs, NFFT = NFFT, noverlap= noverlap, cmap='RdBu_r', vmin=-110, vmax=-30)  
    plt.ylim(0, 4000)  
    plt.colorbar(label='Intensidad (dB)')
    plt.title(f'Espectrograma de banda angosta de {nombre}')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Frecuencia (Hz)')
    plt.tight_layout()
    plt.show()

def espectrograma_ancha(seg, fs, nombre):

    NFFT = min(512, len(seg)//4)
    overlap = 0.95

    noverlap = int(NFFT*overlap)  

    figsize = (10, 6)
    plt.figure(figsize=figsize)
    plt.specgram(seg, Fs=fs, NFFT = NFFT, noverlap= noverlap, cmap='RdBu_r', vmin=-110, vmax=-30) 
    plt.ylim(0, 4000)  
    plt.colorbar(label='Intensidad (dB)')
    plt.title(f'Espectrograma de banda ancha de {nombre}')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Frecuencia (Hz)')
    plt.tight_layout()
    plt.show()


#################################################################################################

espectrograma_angosta_completo(x, fs)
espectrograma_ancha_completo(x, fs)
espectrograma_angosta(seg_A1, fs, "A1")
espectrograma_angosta(seg_A2, fs, "A2")
espectrograma_angosta(seg_o, fs, "O")
espectrograma_ancha(seg_A1, fs, "A1")
espectrograma_ancha(seg_A2, fs, "A2")
espectrograma_ancha(seg_o, fs, "O")




