from cipher.config import ConfigFile
from os.path import join, dirname

CONFIG_FILE = join(dirname(__file__), 'llm.ini')


class LLMConfig(ConfigFile):
    def __init__(self, filepath):
        ConfigFile.__init__(self, filepath)

    def get_llm_server_inference_url(self):
        return self.get('LLM', 'INFERENCE_URL', fallback='http://localhost:8000')
    
    def set_llm_server_inference_url(self, inference_url: str):
        self.set('LLM', 'INFERENCE_URL', inference_url)

llm_config = LLMConfig(CONFIG_FILE)
