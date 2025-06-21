from subprocess import run
from typing import List, Tuple, Union

from ..abstractionhelper import is_installed, is_wayland
from ..models.action import Action
from ..models.entry import Entry
from ..models.keybinding import Keybinding
from .selector import Selector


class Fuzzel(Selector):
    @staticmethod
    def supported() -> bool:
        return is_wayland() and is_installed("fuzzel")

    @staticmethod
    def name() -> str:
        return "fuzzel"

    def show_selection(
        self,
        entries: List[Entry],
        prompt: str,
        keybindings: List[Keybinding],
        additional_args: List[str],
    ) -> Tuple[Union[Action, None], Union[Entry, None]]:
        fuzzel = run(
            ["fuzzel", "--dmenu", "-p", prompt, *additional_args],
            input="\n".join(self._default_format(entries)),
            capture_output=True,
            encoding="utf-8",
        )

        if fuzzel.returncode == 0:
            return None, self._parse_default_formatted_entry(fuzzel.stdout)
        else:
            return Action.CANCEL, None
