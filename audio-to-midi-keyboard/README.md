# Audio to MIDI Keyboard

This is just a subproject. The goal is to record audio and convert it to a keyboard video live with low latency using the Onsets-Frames model with tensorflow magenta. 

The citation for the Onsets-Frames model paper is here:
`
Hawthorne, C., Elsen, E., Song, J., Roberts, A., Simon, I., Raffel, C., Engel, J., Oore, S., & Eck, D. (2018, June 5). Onsets and Frames: Dual-Objective Piano Transcription. arXiv.org. https://arxiv.org/abs/1710.11153.
`

### Progress:
1. Load the Onsets-Frames model and the pretrained weights.
2. Process the `.wav` and `.mid` files with python.
3. Render a basic video of the keyboard with a naive approach in numpy at >1000fps. More fancy videos may require more advanced methods.
4. Able to display live video with OpenCV Python (60fps OK)
5. Record audio in short segments using `pyaudio` library.
6. Employ a text I/O system for the model and the renderer. Binary files may be more compact in the future. Using a simple OpenCV program to render the data (text files) concurrently into a simple video.


### TODO:
1. Decrease latency when putting together the small segments.
2. Write code with more flexibility regarding resolution, frame rate, colors, and other changes.
3. Render better looking videos.


### Installation and Usage:

1. Run `pip install -r requirements.txt`
2. Make sure to have OpenCV installed (https://opencv.org/releases/). Locate the library and include directories then run `python compile.py`
3. Download the pretrained weights for Onsets-Frames and place the `checkpoint`, `model.ckpt.data-00000-of-00001`, `model.ckpt.index`, and `model.ckpt.meta` files into a folder named `onsets-frames`. 
4. Ensure ramdisk is configured. `sudo mkdir /mnt/ramdisk` and `sudo mount -t tmpfs -o rw,size=2G tmpfs /mnt/ramdisk` on ubuntu.
5. Run `python app.py & ./render [optional delay (in seconds)]`
