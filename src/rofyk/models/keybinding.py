from dataclasses import dataclass

from .action import Action


@dataclass
class Keybinding:
    shortcut: str
    action: Action | None
