import os
from cipher.config import ConfigFile
from os.path import join, dirname

CONFIG_FILE = join(dirname(__file__), 'voice.ini')
VOICES_DIR = join(dirname(__file__), 'voices')

class VoiceConfig(ConfigFile):
    def __init__(self, filepath):
        ConfigFile.__init__(self, filepath)
        
    def get_voice(self):
        return self.get('VOICE', 'NAME', fallback=None)
    
    def set_voice(self, voice: str):
        self.set('VOICE', 'NAME', voice)

voice_config = VoiceConfig(CONFIG_FILE)

# Ensure voices directory exists
os.makedirs(VOICES_DIR, exist_ok=True)
