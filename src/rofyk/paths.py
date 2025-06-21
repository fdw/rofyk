import os
from pathlib import Path

if os.environ.get("XDG_CACHE_HOME"):
    cache_file = Path(os.environ.get("XDG_CACHE_HOME")) / "rofyk.runcache"
else:
    cache_file = Path.home() / ".cache" / "rofyk.runcache"

if os.environ.get("XDG_CONFIG_HOME"):
    config_home = Path(os.environ.get("XDG_CONFIG_HOME"))
else:
    config_home = Path.home() / ".config"

if os.environ.get("XDG_CONFIG_DIRS"):
    config_global = [Path(dir) for dir in os.environ.get("XDG_CONFIG_DIRS").split(":")]
else:
    config_global = [Path("/etc/xdg")]

config_file_locations = [str(directory / "rofyk.rc") for directory in [config_home] + config_global]
