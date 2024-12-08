from pathlib import Path

from .base import Command


class TestArg:
    pass


class TestCommand(Command[TestArg]):
    @staticmethod
    def parse(args):
        pass

    def run(self):
        with open("orkestr8_mock.py", "w") as server_script:
            current_loc = Path(__file__).parent.parent
            with open(current_loc / "test_script.py") as f:
                data = f.read()
            server_script.write(data)
