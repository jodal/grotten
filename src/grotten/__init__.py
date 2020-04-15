import gettext
from pathlib import Path


gettext.bindtextdomain("messages", str(Path(__file__).parent / "locale"))
gettext.textdomain("messages")
