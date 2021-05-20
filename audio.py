import os
import librosa
import librosa.display
import IPython.display as ipd
import numpy as np
import matplotlib.pyplot as plt


scale_file = "audio.wav"

scale, sr = librosa.load(scale_file)

mel = librosa.feature.melspectrogram(scale, sr=sr, n_mels=240)
lm = librosa.power_to_db(mel)
plt.figure(figsize=(25,10))
librosa.display.specshow(lm, x_axis='time', y_axis='mel', sr=sr)
plt.colorbar(format="%+2.f")
plt.show()

