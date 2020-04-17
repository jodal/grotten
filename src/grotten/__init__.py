import gettext
import importlib.metadata
from pathlib import Path


__version__ = importlib.metadata.version("grotten")


gettext.bindtextdomain("messages", str(Path(__file__).parent / "locale"))
gettext.textdomain("messages")
