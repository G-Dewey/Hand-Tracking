import config
from datetime import datetime
from pathlib import Path

class Debugger:
    def __init__(self):
        self.log_enabled = config.DEBUG_LOG
        self.console_enabled = config.DEBUG_CONSOLE

        # Creates log file if logging is enabled
        if self.log_enabled:
            logs_folder = Path(__file__).parent / config.LOGS_FOLDER_PATH
            logs_folder.mkdir(exist_ok=True)
            filename = logs_folder / f"debug_{datetime.now():%Y%m%d_%H%M%S}.log"
            self.log_file = open(filename, "a", encoding="utf-8")

    def __del__(self):
        if self.log_enabled:
            self.log_file.close()

    def log(self, message):
        if self.log_enabled:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log_file.write(f"[{timestamp}] {message}\n")
            self.log_file.flush()  # Ensure the message is written to the file immediately

        if self.console_enabled:
            print(message)

debug = Debugger()   
            
