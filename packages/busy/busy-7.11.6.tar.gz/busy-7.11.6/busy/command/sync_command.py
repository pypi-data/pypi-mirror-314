from importlib import import_module
from busy.command import BusyCommand, IntegrationCommand

from wizlib.parser import WizParser

from busy.error import BusyError


class SyncCommand(BusyCommand, IntegrationCommand):
    """Takes the name of an integration"""

    name = 'sync'

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        parser.add_argument('integration')

    @BusyCommand.wrap
    def execute(self):
        return self.execute_integration()
