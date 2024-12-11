from wizlib.command import WizCommand
from wizlib.parser import WizParser
from wizlib.ui import Choice, Chooser
from wizlib.command import CommandCancellation


class SwytchitCommand(WizCommand):

    default = 'start'

    # TODO: Move to wizlib
    def confirm(self, verb, *other_actions):  # pragma: nocover
        """Ensure that a command is confirmed by the user"""
        if self.provided('yes'):
            return self.yes
        else:
            def cancel():
                raise CommandCancellation('Cancelled')
            chooser = Chooser(f"{verb}?", 'OK', [
                Choice('OK', '\n', True),
                Choice('cancel', 'c', cancel)
            ])
            for action in other_actions:
                name = action.name if hasattr(action, 'name') else 'other'
                key = action.key if hasattr(action, 'key') else 'o'
                chooser.add_choice(name, key, action)
            choice = self.app.ui.get_option(chooser)
            if type(choice) is bool:
                self.yes = choice
            return choice
