
from argparse import ArgumentParser
import os
from pathlib import Path
import subprocess
import sys
from tempfile import NamedTemporaryFile
from swytchit.command import SwytchitCommand

import wizlib

from swytchit.error import SwytchitError

RCFILE = '.swytchitrc.sh'


class StartCommand(SwytchitCommand):
    name = 'start'

    @classmethod
    def add_args(self, parser: ArgumentParser):
        parser.add_argument('directory')

    def handle_vals(self):
        super().handle_vals()
        if not wizlib.io.isatty():
            raise SwytchitError('Swytchit only works in interactive tty')
        self.dirpath = Path(self.directory).expanduser().resolve()
        if not (self.dirpath.is_dir()):
            raise SwytchitError(
                'Swytchit requires an existing directory as an argument')
        if not (self.dirpath.is_relative_to(Path.home())):
            raise SwytchitError(
                'Swytchit only operates within user home directory')

    @SwytchitCommand.wrap
    def execute(self):
        shell = self.app.config.get('swytchit-shell') or os.getenv('SHELL')
        parents = [d for d in self.dirpath.parents]
        with NamedTemporaryFile(mode='w+t', delete=False) as rcfile:
            rcfile.write('unset SWYTCHITRC\n')
            for path in reversed([self.dirpath] + parents):
                if path.is_relative_to(Path.home()):
                    if (path / RCFILE).is_file():
                        with open(path / RCFILE) as file:
                            rcfile.write(file.read() + '\n')
            rcfile.seek(0)
            os.environ['SWYTCHITRC'] = rcfile.name
            os.chdir(self.dirpath)
            subprocess.run([shell])
