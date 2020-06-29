import json
import numpy as np
from os.path import exists, join
from keras.models import load_model

from . import speech
from .recorder.constants import TRAINED_MODEL_PATH, DATASET_PATH, SAMPLERATE, WAKE_WORD_CLASS, DETECT_THRESHOLD
from .recorder.features import SELECTED_FEATURE, N_SAMPLE_MFCCS, N_MFCC
from .recorder.listener import Listener
from .recorder.processes import pre_process
from .recorder.reader import get_labels
from cipher.core.sequence_reader import sequence_reader
from .model import Intent

from librosa.output import write_wav

def predict(model, data):
    data_reshaped = data.reshape(1, N_SAMPLE_MFCCS, N_MFCC)
    prediction = model.predict(data_reshaped)
    
    max_accuracy = np.max(prediction)

    print(max_accuracy)
    print(get_labels()[np.argmax(prediction)])
    if max_accuracy < DETECT_THRESHOLD:
        return None
    best_class_index = np.argmax(prediction)

    return get_labels()[best_class_index]

def start_recognition():
    if exists(TRAINED_MODEL_PATH):
        speech.log.info("Loading model ...")
        model = load_model(TRAINED_MODEL_PATH)
    else:
        speech.log.error("No model found ! Exiting ...")
        return False

    def on_wake_word():
        """
        Function called when the wake word is detected.
        """
        rec = listener.record()
        rec = pre_process(rec)
        prediction = predict(model, SELECTED_FEATURE(rec))
        if prediction is not None:
            speech.log.info("Intent '%s' detected.", prediction)
            db_intent = Intent.query.filter_by(intent=prediction).first()

            if(db_intent is not None):
                if db_intent.sequence is not None:
                    sequence_reader.launch_sequence(db_intent.sequence.id)

        else:
            speech.log.debug("No intent detected, maybe the threshold is too low ?")
            write_wav('test.wav', rec, SAMPLERATE)


    def on_noise(data):
        """
        Function called when some noise is detected in the microphone.
        """
        speech.log("Noise detected")
        write_wav('./test1.wav', data, SAMPLERATE) # Save as WAV file

        data = pre_process(data)
        write_wav('./test.wav', data, SAMPLERATE) # Save as WAV file

        prediction = predict(model, SELECTED_FEATURE(data))
        if prediction == WAKE_WORD_CLASS:
            speech.log.info("Wake word detected")
            on_wake_word()

    listener = Listener(on_noise)
    #listener.start()
    speech.log.info("Recording started")

start_recognition()