import numpy as np
from librosa.effects import trim, split
from .constants import SAMPLERATE, DEFAULT_SAMPLE_DURATION

#def ambiant_noice_reduction(data):
    # Divide the audio in frames of 25ms with hop length of 10ms.
    #frames = frame(data, frame_length=round(SAMPLERATE*(0.025/60)), hop_length=round(SAMPLERATE*(0.010/60)))
    # Calculate the spectral centroids for each window.
   # centroids = spectral_centroid(y=data, sr=SAMPLERATE, win_length=round(SAMPLERATE*(0.025/60)), hop_length=round(samplerate*(0.010/60)))
    ##centroids = [spectral_centroid(y=f, sr=SAMPLERATE) for f in frames]
    #lower_threshold = np.min(centroids)
    #upper_threshold = np.max(centroids)
    # Apply a lowshelf filter for gain=-30 and frequency as the lower threshold. Apply a highshelf filter for gain=-30 and higher threshold.
    # Apply limiter with a gain of +10 to increase the volume.
    #less_noise = AudioEffectsChain().lowshelf(gain=-30.0, frequency=lower_threshold, slope=0.5).highshelf(gain=-30.0, frequency=upper_threshold, slope=0.5).limiter(gain=20.0)
    #data_cleaned = less_noise(data)
    #return data_cleaned

def pre_process(data):
    #data = ambiant_noice_reduction(data)
    #data = data[::3] # downsampling
    data, trim_interval = trim(data, top_db=20, frame_length=2048, hop_length=512)
    non_silent_intervals = split(data, top_db=40, frame_length=100, hop_length=25)
    # get only the non silent intervals in the signal
    data = data[non_silent_intervals[0][0]:non_silent_intervals[0][1]]

    padded = np.zeros(SAMPLERATE*DEFAULT_SAMPLE_DURATION)
    # if the sample is too long, cut it
    data = data[:SAMPLERATE*DEFAULT_SAMPLE_DURATION]
    # if the sample is too short, pad it
    padded[:data.shape[0]] = data

    return padded

