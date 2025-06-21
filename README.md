# rofyk
## A rofi (or dmenu) frontend for `ykman`
If you manage your TOTPs with a [Yubikey](https://www.yubico.com/), `rofyk` is a frontend to easily choose and type or copy the TOTP.

## Usage
`rofyk`

# Configuration
You can configure `rofyk` either with cli arguments or with a config file called `$XDG_CONFIG_HOME/rofyk.rc`. In the file, use the long option names without double dashes.

## Options

| long option          | short option | possible values                             | description                                                                                                                                                                                                                                                          |
|----------------------|--------------|---------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--action`           | `-a`         | `type` (default), `copy`, `print`           | Choose what `rofyk` should do.                                                                                                                                                                                                                                    |
| `--prompt`           | `-r`         | any string                                  | Define the text of the prompt.                                                                                                                                                                                                                                       |
| `--keybindings`      |              |                                             | Define custom keybindings in the format `<shortcut>:<action>`, for example `Alt+x:copy`. Multiple keybindings can be concatenated with `,`. Note that `wofi` and `fuzzel` don't support keybindings.                                                                 |
| `--no-cache`         |              |                                             | Disable the automatic frecency cache. It contains sha1-hashes of the selected entries and how often they were used.                                                                                                                                                  |
| `--clear-after`      |              | integer number >= 0 (default is `0`)        | Limit the duration in seconds passwords stay in your clipboard (unless overwritten). When set to 0, passwords will be kept indefinitely.                                                                                                                             |
| `--typing-key-delay` |              | delay in milliseconds                       | Set a delay between key presses when typing. `0` by default, but that may result in problems.                                                                                                                                                                        |
| `--selector-args`    |              |                                             | Define arguments that will be passed through to `rofi`, `wofi`, or `fuzzel`.<br/>Please note that you need to specify it as `--selector-args="<args>"` or `--selector-args " <args>"` because of a [bug in argparse](https://github.com/python/cpython/issues/53580) |
| `--selector`         |              | `rofi`, `wofi`, `fuzzel`, `bemenu`, `dmenu` | Show the selection dialog with this application. Chosen automatically by default.                                                                                                                                                                                    |
| `--clipboarder`      |              | `xsel`, `xclip`, `wl-copy`                  | Access the clipboard with this application. Chosen automatically by default.                                                                                                                                                                                         |
| `--typer`            |              | `xdotool`, `wtype`, `ydotool`, `dotool`     | Type the characters using this application. Chosen automatically by default.                                                                                                                                                                                         |

# Installation

## Manually
Download the wheel file from releases and install it with  `sudo pip install $filename` (or you can use `pip install --user $filename` to only install it for the local user).
Note that it needs `configargparse` to work.

## Dependencies
You also need:
- Python 3.9 or higher
- `rofi`, `wofi`, `fuzzel`, `bemenu` or `dmenu`
- Something to programmatically type characters into other applications. Depending on your display server, it's `xdotool`, `wtype`, `ydotool` or `dotool`.
- Something to copy text to the clipboard. Again, depending on the display server, you want `xclip`, `xsel` or `wl-copy`.
