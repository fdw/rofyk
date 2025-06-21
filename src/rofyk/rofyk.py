from .argument_parsing import parse_arguments
from .cache import Cache
from .clipboarder.clipboarder import Clipboarder
from .models.action import Action
from .selector.selector import Selector
from .typer.typer import Typer
from .ykman import Ykman


class Rofyk(object):
    def __init__(self) -> None:
        self.args = parse_arguments()
        self.ykman = Ykman()
        self.selector = Selector.best_option(self.args.selector)
        self.typer = Typer.best_option(self.args.typer)
        self.clipboarder = Clipboarder.best_option(self.args.clipboarder)
        self.active_window = self.typer.get_active_window()

    def main(self) -> None:
        entries = self.ykman.list_entries()

        if self.args.use_cache:
            cache = Cache()
            entries = cache.sorted(entries)

        (selected_action, selected_entry) = self.selector.show_selection(
            entries,
            self.args.prompt,
            self.args.parsed_keybindings,
            self.args.selector_args,
        )

        if selected_action == Action.CANCEL:
            return

        entry = self.ykman.fetch_credentials(selected_entry)

        if self.args.use_cache:
            cache.update(selected_entry)

        if selected_action is not None:
            self.args.action = selected_action

        self.__execute_action(entry)

    def __execute_action(self, totp: str) -> None:
        if self.args.action == Action.TYPE:
            self.typer.type_characters(totp, self.args.key_delay, self.active_window)
        elif self.args.action == Action.COPY:
            self.clipboarder.copy_to_clipboard(totp)
        elif self.args.action == Action.PRINT:
            print(totp)
