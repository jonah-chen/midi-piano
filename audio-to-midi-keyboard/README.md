# Audio to MIDI Keyboard

This is just a subproject. The goal is to record audio and convert it to a keyboard video live with low latency using the Onsets-Frames model with tensorflow magenta. 

The citation for the Onsets-Frames model paper is here:
`
Hawthorne, C., Elsen, E., Song, J., Roberts, A., Simon, I., Raffel, C., Engel, J., Oore, S., &amp; Eck, D. (2018, June 5). Onsets and Frames: Dual-Objective Piano Transcription. arXiv.org. https://arxiv.org/abs/1710.11153.
`

### Progress:
1. Load the Onsets-Frames model and the pretrained weights.
2. Process the `.wav` and `.mid` files with python.
3. Render a basic video of the keyboard with a naive approach in numpy at >1000fps. More fancy videos may require more advanced methods.
4. Able to display live video with OpenCV Python (60fps OK)

### TODO:
1. Record audio in short (1 to 8 second) continuous segments with low latency.
2. Process the audio with the model and compose small segments of note sequences.
3. Put together the small segments.
4. Render more fancy looking video.


### Installation:

1. Run `pip install -r requirements.txt`
2. Download the pretrained weights for Onsets-Frames and place the `checkpoint`, `model.ckpt.data-00000-of-00001`, `model.ckpt.index`, and `model.ckpt.meta` files into a folder named `onsets-frames`. 
3. Run `python ai.py -h` or `python render.py -h`, then execute the program with specific arguments for your task.
