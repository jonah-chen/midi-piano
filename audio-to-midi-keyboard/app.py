import os
from ai import OnsetsFrames
from render import Seq
from recorder import Recorder
from time import sleep


if __name__ == "__main__":
    model = OnsetsFrames()
    rec = Recorder()
    vid = Seq()

    i = 0
    while 1:
        sleep(1)
        fetched = rec.__fetch__()
        fp = rec.__write__(fetched, filepath="/mnt/ramdisk/tmpaudio")
        sequence = model.predict(fp)
        os.remove(fp)
        f = open(f"/mnt/ramdisk/{i}.txt.tmp", "w")
        f.write(f"{sequence.total_time}\n")
        for note in sequence.notes:
            f.write(f"{note.start_time} {note.end_time} {note.pitch-21}\n")
        f.close()
        os.rename(f"/mnt/ramdisk/{i}.txt.tmp", f"/mnt/ramdisk/{i}.txt")
        i += 1
