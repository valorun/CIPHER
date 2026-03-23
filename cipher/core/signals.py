from blinker import Namespace

_signals = Namespace()

# Triggered when the robot needs to speak
# Arguments: text (str)
speech_synthesized = _signals.signal('speech-synthesized')
