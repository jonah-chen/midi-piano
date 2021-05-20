from tensorflow.keras.models import load_model
import tensorflow as tf

model = load_model('onsets-frames/maestro/train')
model.summary()