from cipher.config import ConfigFile
from os.path import join, dirname

CONFIG_FILE = join(dirname(__file__), 'llm.ini')


class LLMConfig(ConfigFile):
    def __init__(self, filepath):
        ConfigFile.__init__(self, filepath)

    def get_llm_server_address(self):
        return self.get('LLM', 'SERVER_ADDRESS', fallback='localhost')
    
    def set_llm_server_address(self, server_address: str):
        self.set('LLM', 'SERVER_ADDRESS', server_address)

    def get_llm_server_port(self):
        return self.getint('LLM', 'SERVER_PORT', fallback=5000)

    def set_llm_server_port(self, server_port: int):
        self.set('LLM', 'SERVER_PORT', server_port)

llm_config = LLMConfig(CONFIG_FILE)
