import re
from subprocess import run
from typing import List, Tuple, Union

from ..abstractionhelper import is_installed
from ..models.action import Action
from ..models.entry import Entry
from ..models.keybinding import Keybinding
from .selector import Selector


class Rofi(Selector):
    @staticmethod
    def supported() -> bool:
        return is_installed("rofi")

    @staticmethod
    def name() -> str:
        return "rofi"

    def show_selection(
        self,
        entries: List[Entry],
        prompt: str,
        keybindings: List[Keybinding],
        additional_args: List[str],
    ) -> Tuple[Union[Action, None], Union[Entry, None]]:
        parameters = [
            "rofi",
            "-markup-rows",
            "-dmenu",
            "-i",
            "-sort",
            "-p",
            prompt,
            *additional_args,
        ]

        rofi = run(
            parameters,
            input="\n".join(self.__format_entries(entries)),
            capture_output=True,
            encoding="utf-8",
        )

        if rofi.returncode == 1:
            return Action.CANCEL, None
        elif rofi.returncode >= 10:
            keybinding = keybindings[(rofi.returncode - 10)]
            return_action = keybinding.action
        else:
            return_action = None

        return return_action, self.__parse_formatted_string(rofi.stdout)

    def __format_entries(self, entries: List[Entry]) -> List[str]:
        max_width = self._calculate_max_width(entries)
        return [f"<b>{it.name}</b>{self._justify(it, max_width)}  {it.username}" for it in entries]

    def __parse_formatted_string(self, formatted_string: str) -> Entry:
        match = re.compile("<b>(?P<name>.*?) *</b>(?P<username>.*)").search(formatted_string)

        return Entry(match.group("name"), match.group("username").strip())
