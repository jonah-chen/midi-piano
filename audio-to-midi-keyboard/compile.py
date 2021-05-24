OUTPUT_PATH = "render"
INCLUDE_PATH = "/usr/local/include/opencv4"
LIB_PATH = "/usr/local/lib/"

import os
os.system(f"g++ render.cpp -I {INCLUDE_PATH} -L {LIB_PATH} -lopencv_core -lopencv_imgproc -lopencv_videoio -lopencv_highgui -std=c++2a -o {OUTPUT_PATH}")