import numpy as np
from note_seq import midi_io


class Seq:
    START = 0
    END = 1
    PITCH = 2

    def __init__(self, seq=None, init_first=False, frame_rate=30, resolution=(1080, 1920), scroll_time=5, ON=255):
        if seq is None:
            if init_first:
                raise ValueError("Cannot initialize the first frame when no sequence is provided.")
            self.seq = []
        else:
            if type(seq) is str:
                seq = midi_io.midi_file_to_note_sequence(seq)
            self.seq = sorted([(note.start_time, note.end_time, note.pitch - 21)
                            for note in seq.notes])  # sort the notes

        self.frame_rate = frame_rate
        self.rows = [np.zeros(resolution[1], dtype=np.uint8)
                     for _ in range(resolution[0])]
        # The amount of pixels to tick
        self.tick = resolution[0] / (frame_rate * scroll_time)
        # The amount of "real" time that elapses per pixel
        self.tick_rate = scroll_time / resolution[0]
        self.scroll_time = scroll_time

        self.ON = ON

        self.frame = 0
        self.cur_notes = []  # should use an ordered set by end_time of note

        self.mapping = [5 + resolution[1] // 88 * n for n in range(88)]
        self.widths = [resolution[1] // 88 - 5 for _ in range(88)]

        # Initialize first frame
        if init_first:
            for _ in range(int(frame_rate*scroll_time)):
                self.__next__()

    def __iter__(self):
        """Python is dumb.

        Returns:
            dummy iterator
        """
        return self

    def __next__(self):
        """Return the next frame for the keyboard video generated by the note sequence 
        using a naive approach and numpy. 

        Returns:
            numpy.array: The next frame of the keyboard video.
        """
        # Real program will probably use pointer hack
        # but here we'll just take the naive approach
        
        # Update the frame
        self.frame = self.frame + 1

        for tick in range(int((self.frame - 1) * self.tick), int(self.frame * self.tick)):
            # Remove the first useless rows
            del self.rows[0]
            time = tick * self.tick_rate

            # Remove the notes that has already stopped:
            i = 0
            while i < len(self.cur_notes):
                if self.cur_notes[i][Seq.END] <= time:
                    del self.cur_notes[i]
                else:
                    i = i + 1

            # Add the new notes being played
            while self.seq and self.seq[0][Seq.START] <= time:
                self.cur_notes.append(self.seq.pop(0))

            # Append the new rows
            new_row = np.zeros(self.rows[0].shape, dtype=np.uint8)
            for note in self.cur_notes:
                new_row[self.mapping[note[Seq.PITCH]]:self.mapping[note[Seq.PITCH]
                                                                   ]+self.widths[note[Seq.PITCH]]] = self.ON

            self.rows.append(new_row)

        return np.array(self.rows, dtype=np.uint8)

    def __time__(self):
        """Find the time of this frame.

        Returns:
            float: Time this frame occurs in seconds.
        """
        return self.frame / self.frame_rate - self.scroll_time

    def __add__(self, new_note_seq):
        for note in new_note_seq.notes:
            self.seq.append((note.start_time, note.end_time, note.pitch - 21))
            



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description="Render a MIDI file to a virtual keyboard video")
    parser.add_argument("infile", type=str,
                        help="file path of the input file (excluding the .wav extention)")
    parser.add_argument("--fps", dest="show_fps",
                        action="store_const", const=True, default=False)
    args = parser.parse_args()

    from cv2 import cv2
    from time import perf_counter

    s = Seq(f"{args.infile}.wav")
    while 1:
        if args.show_fps:
            t = perf_counter()
        frame = next(s)
        if args.show_fps:
            print(f"Live: {1/(perf_counter()-t)}fps")
        cv2.imshow('frame', np.flip(frame, axis=0))
        k = cv2.waitKey(25)
        if k == ord('q'):
            break
