from subprocess import Popen

from ..BaseUI import BaseClass
from pytessng.Config import PathConfig


class OpenExamples(BaseClass):
    name = "打开路网创建样例"

    def load(self):
        Popen(['explorer', PathConfig.EXAMPLES_DIR_PATH], shell=True)
