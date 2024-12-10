from webbrowser import open

from ..BaseUI import BaseClass
from pytessng.Config import PathConfig


class OpenInstruction(BaseClass):
    name = "打开用户说明书"

    def load(self):
        open(PathConfig.INSTRUCTION_FILE_PATH, new=2)
