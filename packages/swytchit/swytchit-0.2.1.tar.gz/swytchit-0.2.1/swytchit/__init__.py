import sys
from wizlib.app import WizApp
from wizlib.ui_handler import UIHandler
from wizlib.config_handler import ConfigHandler

from swytchit.command import SwytchitCommand


class SwytchitApp(WizApp):

    base = SwytchitCommand
    name = 'sw'
    handlers = [UIHandler, ConfigHandler]
