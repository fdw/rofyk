from subprocess import run
from typing import List, Tuple, Union

from ..abstractionhelper import is_installed
from ..models.action import Action
from ..models.entry import Entry
from ..models.keybinding import Keybinding
from .selector import Selector


class Bemenu(Selector):
    @staticmethod
    def supported() -> bool:
        return is_installed("bemenu")

    @staticmethod
    def name() -> str:
        return "bemenu"

    def show_selection(
        self,
        entries: List[Entry],
        prompt: str,
        keybindings: List[Keybinding],
        additional_args: List[str],
    ) -> Tuple[Union[Action, None], Union[Entry, None]]:
        bemenu = run(
            ["bemenu", "-p", prompt, *additional_args],
            input="\n".join(self._default_format(entries)),
            capture_output=True,
            encoding="utf-8",
        )

        if bemenu.returncode == 0:
            return None, self._parse_default_formatted_entry(bemenu.stdout)
        else:
            return Action.CANCEL, None
