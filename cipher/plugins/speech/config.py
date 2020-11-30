from cipher.config import ConfigFile
from os.path import join, dirname

CONFIG_FILE = join(dirname(__file__), 'voice.ini')

class VoiceEffect():
    def __init__(self, name, param_name, min_value, max_value, default_value, config):
        self.name = name
        self.param_name = param_name
        self.MIN = min_value
        self.MAX = max_value
        self.DEFAULT = default_value
        self.config = config

    def get(self):
        return self.config.getfloat(self.name, 'VALUE', fallback=self.DEFAULT)
    
    def set(self, value: float):
        if value is None or value < self.MIN:
            value = self.MIN
        if value > self.MAX:
            value = self.MAX
        self.config.set(self.name, 'VALUE', value)
        return self

    def is_enabled(self):
        return self.config.getboolean(self.name, 'ENABLED', fallback=False)

    def enable(self, value: bool):
        if value is not True and value is not False:
            value = False
        self.config.set(self.name, 'ENABLED', value)
        return self

class VoiceConfig(ConfigFile):
    def __init__(self, filepath):
        ConfigFile.__init__(self, filepath)
        self.effects = {
            'Volume': VoiceEffect('VOLUME', 'amount', 0.0, 10.0, 1.0, self),
            'TractScaler' : VoiceEffect('TRACT_SCALER', 'amount', 0.25, 4.0, 1.5, self),
            'F0Scale' : VoiceEffect('F0_SCALE', 'f0Scale', 0.0, 3.0, 2.0, self),
            'F0Add' : VoiceEffect('F0_ADD', 'f0Add', -300.0, 300.0, 50.0, self),
            'Rate' : VoiceEffect('RATE', 'durScale', -0.1, 3.0, 1.5, self),
            'Robot' : VoiceEffect('ROBOT', 'amount', 0.0, 100.0, 100.0, self),
            'Whisper' : VoiceEffect('WHISPER', 'amount', 0.0, 100.0, 100.0, self),
            'Stadium' : VoiceEffect('STADIUM', 'amount', 0.0, 200.0, 100.0, self)
        }
        self.SERVER_ADDRESS = 'marytts'
        self.SERVER_PORT = 59125

    def get_voice(self):
        return self.get('VOICE', 'NAME', fallback=None)
    
    def set_voice(self, voice: str):
        self.set('VOICE', 'NAME', voice)

voice_config = VoiceConfig(CONFIG_FILE)
