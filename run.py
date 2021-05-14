infile = "testing.mp4"
outfile = "test"

import os

def compile(name="process"):
    os.system(f"g++ process.cpp -I /usr/local/include/opencv4 -L /usr/local/lib/ -lopencv_core -lopencv_imgproc -lopencv_videoio -lopencv_highgui -o {name}")

os.remove(outfile)
f = open(outfile, "x")

os.system(f"./process {infile} {outfile}")