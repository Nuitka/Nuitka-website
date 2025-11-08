from configparser import ConfigParser

CONFIG_FILE = "settings.ini"
config = ConfigParser()
config.read(CONFIG_FILE)

comparison_threshold = config.getint("DEFAULT", "COMPARISON_THRESHOLD", fallback=15)

STATE_FILE = "state.ini"
config = ConfigParser()
config.read(STATE_FILE)

development_mode = config.getboolean("DEFAULT", "DEVELOPMENT_MODE", fallback=False)
