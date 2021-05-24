import pyaudio
import wave
from time import sleep, time_ns


class Recorder:
    def __init__(self, buffer_sz=2048, sample_type=pyaudio.paInt16):
        self.buffer = []
        self.buffer_sz = buffer_sz
        self.sample_type = sample_type
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=sample_type, channels=1, rate=44100, input=True, frames_per_buffer=self.buffer_sz)


    def __start__(self):
        """Start the recording stream
        """
        self.stream.start_stream()

    def __stop__(self):
        """Stop the recording stream
        """
        self.stream.stop_stream()

    def __fetch__(self, num=None, output=True):
        """Fetch the num frames of audio to a list of bytes.

        Args:
            num (int, optional): The number of buffers to fetch. Defaults to None which fetches all available buffers.
            output (bool, optional): Whether to write the buffers into self.buffers or return it as a list. Defaults to True.

        Returns:
            void: if output is false
            list[bytes]: if output is true, containing the requested audio data.
        """
        if output:
            out = []
            if num is None:
                while self.stream.get_read_available() >= self.buffer_sz:
                    out.append(self.stream.read(self.buffer_sz))
                return out
            for i in range(num):
                if not self.stream.get_read_available():
                    print(
                        f"Trying to read {num} blocks, but only {i+1} blocks is available.")
                    return out
                out.append(self.stream.read(self.buffer_sz))
            return out

        if num is None:
            while self.stream.get_read_available():
                self.buffer.append(self.stream.read(self.buffer_sz))
        else:
            for i in range(num):
                if not self.stream.get_read_available():
                    print(
                        f"Trying to read {num} blocks, but only {i+1} blocks is available.")
                    break
                self.buffer.append(self.stream.read(self.buffer_sz))

    def __getbuffer__(self, empty=True):
        """Get the data from the buffer stored in self.buffer.

        Args:
            empty (bool, optional): Whether or not to empty the self.buffer. Defaults to True.

        Returns:
            list[bytes]: All the audio data that has been stored into the buffer.
        """
        tmp = self.buffer
        if empty:
            self.buffer = []
        return tmp

    def __write__(self, data, filepath=None):
        if filepath is None:
            filepath = str(time_ns())
        filepath += ".wav"
        sound_file = wave.open(filepath, "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(self.audio.get_sample_size(self.sample_type))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(data))
        sound_file.close()
        return filepath

    def __convert_seconds__(self, seconds):
        return int(seconds * 44100 / self.buffer_sz)


if __name__ == '__main__':
    r = Recorder()
    frames = r.__convert_seconds__(5)
    sleep(5)
    fetched = r.__fetch__(frames)
    r.__write__(fetched)
