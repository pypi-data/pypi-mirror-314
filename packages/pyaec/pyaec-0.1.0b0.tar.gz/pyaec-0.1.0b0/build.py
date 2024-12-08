from typing import Any
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
import os


class SpecialBuildHook(BuildHookInterface):
    PLUGIN_NAME = "platform specific"

    def __init__(self, *args):
        print(__file__)
        print(os.getcwd())
        print(args)
        super().__init__(*args)

    def initialize(self, version, build_data):
        # Wheel is platform specific!
        build_data["pure_python"] = False

        # Create platform specific named wheel!
        # https://docs.python.org/3/library/sysconfig.html#sysconfig.get_platform
        # https://peps.python.org/pep-0425/
        # py3-none-win-amd64
        # py3-none-linux_x86_64
        # py3-none-macosx_14_0_x86_64
        # env_wheel_tag = os.getenv("WHEEL_TAG")
        # if env_wheel_tag:
        #     build_data["tag"] = env_wheel_tag
        # else:
        #     # Strict tag to OS and Python version
        #     build_data["infer_tag"] = True
