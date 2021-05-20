# MIDI Piano Conversion with Computer Vision

This project will attempt to perform data acquisition using some webcam(s) on a grand piano in order to convert the notes to MIDI-like format. I also have an extra computer laying around with an old Pentium G3258 and 16GB of memory, which I can dedicate to this task.

### Roadmap

1. Experiment with some methodology of processing the webcam data of the piano's hammers in a way that can be robust to lighting changes, small vibrations, and the movements of nearby hammers.
2. Design the hardware component of the system, including the webcam mounts and additional supplemental components (like reference markers).
3. Integrate the hardware into the system and tune hyperparameters (sampling rate, resolution, etc.). This way, a working data acquisition system can be used and tested for rohbustness. Also potentially convert opencv code to C++ if a significant performance increase is required.
4. Processing the data acquired into a compact and usable format (not necessarily MIDI, but that would also be nice). The saved data can be used to construct datasets to be used in the future.
5. Implement various statistical analysis techniques to analyze what is being played.
6. Implement a graphical program that can compare what is played to the score itself.

### Progress
1. Learn to process videos and webcam with opencv.
2. Converted the basic kernels from opencv python version to opencv C++ version.
3. Using the Onsets and Frames from the Magenta-Tensorflow framework, create a naive audio to MIDI converter which may be able to extract some helpful data. 

### Issues

1. Increase camera FPS from 30 to 60. Test trials using better camera. Minimum price: $40/camera?
2. Opencv webcam is not sampling fast enough. Need to use a better video capture software then process in opencv. It is okay if the processing is ~60000ms behind.