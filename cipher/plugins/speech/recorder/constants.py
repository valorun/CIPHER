from os.path import join, dirname

DATASET_PATH=join(dirname(__file__), 'dataset/')

TRAINED_MODEL_PATH=join(dirname(__file__), 'trained_model')

SAMPLERATE = 16000  # Sample rate
CHANNELS = 1
DEFAULT_SAMPLE_DURATION = 3  # Duration of recording
NOISE_THRESHOLD = 0.1

DETECT_THRESHOLD = 0.5

SPEECH_TIMEOUT = 1

WAKE_WORD_CLASS = 'WAKE_WORD'