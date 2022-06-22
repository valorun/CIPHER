from os.path import isfile, join, exists, dirname
from configparser import ConfigParser, _UNSET
from .constants import CONFIG_FILE

class ConfigFile(ConfigParser):
    """
    Class used to generate and manage a config file
    """
    def __init__(self, filepath):
        ConfigParser.__init__(self)
        self.filepath = filepath
        if exists(filepath):
            self.read(filepath)

    def set(self, section: str, option: str, data):
        """
        Save an option into the config file.
        """
        if not self.has_section(section):
            self.add_section(section)
        ConfigParser.set(self, section, option, str(data))
        with open(self.filepath, 'w') as f:
            self.write(f)

    def getlist(self, section: str, option: str, raw=False, vars=None, fallback=_UNSET):
        return self.get(section, option, fallback=fallback).split(',')



class CoreConfig(ConfigFile):

    def __init__(self, filepath):
        ConfigFile.__init__(self, filepath)

        # MQTT BROKER URL
        self.MQTT_BROKER_URL = self.get('MQTT_BROKER', 'URL',
            fallback='localhost')

        # MQTT BROKER PORT
        self.MQTT_BROKER_PORT = self.getint('MQTT_BROKER', 'PORT',
                fallback=1883)

        # SERVER DATABASE
        self.DATABASE_FILE = self.get('SERVER', 'DATABASE_FILE',
                fallback='sqlite:///' + join(dirname(__file__), 'server_data.db'))

        # LOG FILE
        self.LOG_FILE = self.get('SERVER', 'LOG_FILE',
                fallback=join(dirname(__file__), 'app.log'))

        # SOUNDS LOCATION
        self.SOUNDS_LOCATION = self.get('SERVER', 'SOUNDS_LOCATION',
                fallback=join(dirname(__file__), 'sounds/'))
        
        # DEBUG
        self.DEBUG = self.getboolean('GENERAL', 'DEBUG',
                fallback=False)

        # PLUGINS
        self.PLUGINS = self.getlist('SERVER', 'PLUGINS',
                fallback='dashboard,commands,speech,hearing,sequences,settings')  # all plugins to load, corresponds to the different pages available on the navbar

        # CAMERA FRAME RATE (Hz)
        self.CAMERA_FRAME_RATE = self.getint('GENERAL', 'CAMERA_FRAME_RATE',
                fallback=30)

    # AUDIO SOURCE
    def set_audio_on_server(self, mode: bool):
        self.set('GENERAL', 'AUDIO_ON_SERVER', mode)

    def get_audio_on_server(self) -> bool:
        return self.getboolean('GENERAL', 'AUDIO_ON_SERVER',
            fallback=False)

    # MOTION RASPI ID
    def set_motion_raspi_id(self, raspi_id: str):
        if not raspi_id.strip():
            raspi_id = ''
        self.set('GENERAL', 'MOTION_RASPI_ID', raspi_id)

    def get_motion_raspi_id(self) -> str:
        value = self.get('GENERAL', 'MOTION_RASPI_ID', 
            fallback=None)
        if value == '':
            value = None
        return value

    # ROBOT NAME
    def set_robot_name(self, name: str):
        if not name.strip():
            name = 'My robot'
        self.set('GENERAL', 'ROBOT_NAME', name)

    def get_robot_name(self) -> str:
        return self.get('GENERAL', 'ROBOT_NAME', 
            fallback='My robot')

    # ENABLE MOTION
    def set_enable_motion(self, enable: bool):
        self.set('GENERAL', 'ENABLE_MOTION', enable)

    def get_enable_motion(self) -> bool:
        return self.getboolean('GENERAL', 'ENABLE_MOTION',
            fallback=True)


core_config = CoreConfig(CONFIG_FILE)
