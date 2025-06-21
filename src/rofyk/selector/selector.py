import re
from abc import ABC, abstractmethod
from typing import List, Tuple, Union

from ..models.action import Action
from ..models.entry import Entry
from ..models.keybinding import Keybinding


class Selector(ABC):
    @staticmethod
    def best_option(name: str | None = None) -> "Selector":
        from .bemenu import Bemenu
        from .dmenu import Dmenu
        from .fuzzel import Fuzzel
        from .rofi import Rofi
        from .wofi import Wofi

        available_selectors = [Rofi, Wofi, Fuzzel, Bemenu, Dmenu]

        if name is not None:
            try:
                return next(selector for selector in available_selectors if selector.name() == name)()
            except StopIteration:
                raise NoSelectorFoundException()
        else:
            try:
                return next(selector for selector in available_selectors if selector.supported())()
            except StopIteration:
                raise NoSelectorFoundException()

    @staticmethod
    @abstractmethod
    def supported() -> bool:
        pass

    @staticmethod
    @abstractmethod
    def name() -> str:
        pass

    @abstractmethod
    def show_selection(
        self,
        entries: List[Entry],
        prompt: str,
        keybindings: List[Keybinding],
        additional_args: List[str],
    ) -> Tuple[Union[Action, None], Union[Entry, None]]:
        pass

    @staticmethod
    def _calculate_max_width(entries: List[Entry]) -> int:
        return max(len(it.name) for it in entries)

    @staticmethod
    def _justify(entry: Entry, max_width: int) -> str:
        whitespace_length = max_width - len(entry.name)
        return " " * whitespace_length

    def _default_format(self, entries: List[Entry]) -> List[str]:
        max_width = self._calculate_max_width(entries)
        return [f"{it.name}{self._justify(it, max_width)}  {it.username}" for it in entries]

    def _parse_default_formatted_entry(self, formatted_entry: str) -> Entry:
        match = re.compile("(?P<name>.*?) *  (?P<username>.*)").search(formatted_entry)

        return Entry(match.group("name").strip(), match.group("username").strip())


class NoSelectorFoundException(Exception):
    def __str__(self) -> str:
        return "Could not find a valid way to show the selection. Please check the required dependencies."
