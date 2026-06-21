import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

# vocales son periodicas armónicas entonces es un tren de impulsos y el resto es ruido 

audio_lento = "lento2.wav"

fs_lento, x_lento = wavfile.read(audio_lento)

x_lento = x_lento / np.max(np.abs(x_lento))#limito la amplitud -1 a 1
t_lento = np.arange(len(x_lento)) / fs_lento


plt.plot(t_lento, x_lento, linewidth = 0.8)
plt.xlabel("Tiempo", fontsize=15.0)
plt.ylabel("Amplitud", fontsize=15.0)
plt.title("Señal de voz lenta", fontsize=20.0)
plt.show()

#hace un coloreo sobre las partes de interés 
plt.plot(t_lento, x_lento, linewidth = 0.8)

plt.axvspan(0.705, 1.698, alpha=0.25, color='green')
plt.axvspan(2.151, 2.291, alpha=0.25, color= 'red')
plt.axvspan(2.308, 2.980, alpha=0.25, color='green')
plt.axvspan(3.404, 3.549, alpha=0.25, color='red')
plt.axvspan(3.558, 4.339, alpha=0.25, color= 'green')
plt.axvspan(4.351, 5.213, alpha=0.25, color='red')

plt.xlabel("Tiempo", fontsize=15.0)
plt.ylabel("Amplitud", fontsize=15.0)
plt.title("Señal de voz lenta", fontsize=20.0)
plt.show()
