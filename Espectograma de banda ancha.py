import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

fs, x = wavfile.read("lento2.wav")
x = x / np.max(np.abs(x))

NFFT = int(512)       
overlap = 0.9      

noverlap = int(NFFT*overlap)  
figsize = (10, 6)
plt.figure(figsize=figsize)
plt.specgram(x, Fs=fs, NFFT=NFFT, noverlap=noverlap, cmap='gray', vmin=-110, vmax=-30)  
plt.ylim(0, 4000)  
plt.colorbar(label='Intensidad (dB)')
plt.title('Espectrograma de banda ancha de toda la palabra')
plt.xlabel('Tiempo (s)')
plt.ylabel('Frecuencia (Hz)')
plt.tight_layout()
plt.show()
