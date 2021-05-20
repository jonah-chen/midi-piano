infile = "angle.mp4"
outfile = "test.csv"

import os

def compile(name="process"):
    os.system(f"g++ process.cpp -I /usr/local/include/opencv4 -L /usr/local/lib/ -lopencv_core -lopencv_imgproc -lopencv_videoio -lopencv_highgui -o {name}")
if __name__ == "__main__":
    compile()
    os.remove(outfile)
    f = open(outfile, "x")
    f.close()

    os.system(f"./process {infile} {outfile}")