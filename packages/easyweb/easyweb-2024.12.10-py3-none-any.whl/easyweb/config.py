import os
import pathlib


class Config:
    HOME = str(pathlib.Path.home())
    USER_DATE_DIR = f"{HOME}/.config/browser"
    EXECUTABLE_PATH = "/usr/bin/browser"
    HEADLESS = bool(os.getenv('HEADLESS'))

config = Config()
