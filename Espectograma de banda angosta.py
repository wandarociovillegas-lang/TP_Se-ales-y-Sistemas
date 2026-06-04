#Espectograma de banda angosta
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

fs, x = wavfile.read("lento2.wav")
x = x / np.max(np.abs(x))

NFFT = int(20480)       # Tamaño de la ventana   #cuántas muestras de la señal se toman para hacer cada FFT local.
overlap = 0.9      # Solapamiento entre ventanas consecutivas -> continuidad en la imagen

noverlap = int(NFFT*overlap)  #convierte porcentaje de continuidad de la imagen en número de muestras
figsize = (10, 6)
plt.figure(figsize=figsize)
plt.specgram(x, Fs=fs, NFFT=NFFT, noverlap=noverlap, cmap='gray', vmin=-110, vmax=-30)  #vmin y vmax limites de dB
plt.ylim(0, 800)  #limita la figura a mostrar 
plt.colorbar(label='Intensidad (dB)')
plt.title('Espectrograma de banda angosta de toda la palabra')
plt.xlabel('Tiempo (s)')
plt.ylabel('Frecuencia (Hz)')
plt.tight_layout()
plt.show()
