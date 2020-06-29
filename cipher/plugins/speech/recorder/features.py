from librosa.feature import mfcc
from .constants import SAMPLERATE
import numpy as np

N_MFCC = 13
N_SAMPLE_MFCCS = 301

def mffcs(data):
    mfccs = mfcc(y=data, sr=SAMPLERATE, n_mfcc=N_MFCC, n_fft=int(SAMPLERATE*0.025), hop_length=int(SAMPLERATE*0.01))
    return np.transpose(mfccs)

SELECTED_FEATURE = mffcs
