import pyaudio
import wave


sound_file = wave.open("template.wav", "wb")
sound_file.setnchannels(1)
sound_file.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
sound_file.setframerate(44100)
sound_file.writeframes(b'')