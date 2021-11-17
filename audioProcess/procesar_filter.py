import tensorflow as tf
from tensorflow import keras
import noisereduce as nr
import matplotlib.pyplot as plt

def print_prueba(f):
    w=get_waveform(f)
    s=get_spectrogram(w)
    print(s)
    plot_spec(s)

def plot_spec(spec):
    plt.figure(figsize=(12, 4))
    plt.imshow(tf.transpose(spec), cmap="viridis")
    plt.colorbar()
    plt.show()
    
def cargar_modelo(route):
  loaded= keras.models.load_model(route)

  return loaded
def reduce_noise(file):
    form,ratio = get_waveform2(file)
    base_noise, ratio_noise= get_waveform2("audios/base_sound.wav")
    reduced_noise = nr.reduce_noise(y=form.numpy(), sr=ratio.numpy(),y_noise=base_noise,n_std_thresh_stationary=1.5,stationary=False)
    return reduced_noise

def preprocess_predict(file):
    x_batch=None
    wave_predict=get_waveform(file)
    wave_predict=reduce_noise(file)
    spec=get_spectrogram(wave_predict)
    spec=tf.expand_dims(spec,axis=0)
    x_batch=spec
    
    return x_batch

def get_waveform(filename):
    raw_audio = tf.io.read_file(filename)
    waveform, ratio = tf.audio.decode_wav(raw_audio,desired_channels=1)
    waveform=tf.squeeze(waveform, axis=-1)
    return waveform

def get_waveform2(filename):
    raw_audio = tf.io.read_file(filename)
    waveform, ratio = tf.audio.decode_wav(raw_audio,desired_channels=1)
    waveform=tf.squeeze(waveform, axis=-1)
    return waveform,ratio

def get_stft(audio, frame_length=2048, frame_step=512, fft_length=256):
    return tf.signal.stft(
        tf.cast(audio, tf.float32),
        frame_length=frame_length,
        frame_step=frame_step,
        fft_length=fft_length
    )
def get_spectrogram(audio):
    audio_stft = get_stft(audio)
    audio_spec = tf.abs(audio_stft)
    return tf.math.log(tf.transpose(audio_spec))

def lab_to_class(label):
    if label==1:
      return "glass"
    else:
      return "plastic"

def predict(loaded,x_pred):
  preds= loaded.predict(x_pred)
  print(preds)
  pred_classes= tf.squeeze(tf.cast(preds>0.5,tf.int8))
  predicted_lab=pred_classes.numpy()
  print(predicted_lab)
  return predicted_lab

def process():
  pred_route="predictions/pred.wav"
  model_route="models/"
  modelo= cargar_modelo(model_route)
  X_prediction= preprocess_predict(pred_route)
  prediction=predict(modelo, X_prediction)
  return prediction