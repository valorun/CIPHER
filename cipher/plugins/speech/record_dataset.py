#!/usr/bin/python3
# coding: utf-8

from recorder.constants import DATASET_PATH, SAMPLERATE, CHANNELS, DEFAULT_SAMPLE_DURATION
from os.path import join, exists
from librosa.output import write_wav
import sounddevice as sd

def record(filename=None):
    record_data = sd.rec(int(DEFAULT_SAMPLE_DURATION * SAMPLERATE), samplerate=SAMPLERATE, channels=CHANNELS)
    sd.wait()  # Wait until recording is finished
    if filename is not None:
        write_wav(filename, record_data, SAMPLERATE) # Save as WAV file
    return record_data

if __name__ == '__main__':
    n_samples = 40
    dir_name = "noise"

    samples_path = join(DATASET_PATH, str(dir_name))

    i = 0
    for n in range(1, n_samples):
        while exists(join(samples_path, str(i) + '.wav')):
            i += 1
        new_file_name = join(samples_path, str(i) + '.wav')
        print("Speak now ... Iteration " + str(n))
        record(new_file_name)
