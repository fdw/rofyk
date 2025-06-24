from subprocess import run
from typing import List

from .models.entry import Entry


class Ykman:
    def list_entries(self) -> List[Entry]:
        rbw = run(["ykman", "oath", "accounts", "list"], encoding="utf-8", capture_output=True)

        if rbw.returncode != 0:
            print("There was a problem calling ykman. Is it installed?")
            print(rbw.stderr)
            exit(12)

        return [self.__parse_ykman_output(it) for it in (rbw.stdout.strip("\n").split("\n"))]

    def __parse_ykman_output(self, entry_string: str) -> Entry:
        fields = entry_string.split(":")

        return Entry(fields[0], fields[1] if len(fields) > 1 else "")

    def fetch_credentials(self, entry: Entry) -> str:
        return run(
            ["ykman", "oath", "accounts", "code", "--single", f"{entry.name}:{entry.username}"],
            capture_output=True,
            encoding="utf-8",
        ).stdout.strip("\n")
