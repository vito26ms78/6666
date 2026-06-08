from config.config_manager import ConfigManager
from logger.file_logger import FileLogger

class Application:

    def __init__(self):

        self.config = ConfigManager().load()
        self.logger = FileLogger()

    def startup(self):

        self.logger.info(
            "Anber Translator V1 Startup"
        )

        return self.config
