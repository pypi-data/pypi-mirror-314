import sys
from wizlib.app import WizApp
from wizlib.ui_handler import UIHandler
from wizlib.config_handler import ConfigHandler

from busy.command import BusyCommand
from busy.storage.file_storage import FileStorage


class BusyApp(WizApp):

    base = BusyCommand
    name = 'busy'
    handlers = [UIHandler, ConfigHandler]

    def __init__(self, **handlers):
        super().__init__(**handlers)
        self.storage = FileStorage(self.config.get('busy-storage-directory'))

    def run(self, **vals):
        super().run(**vals)
