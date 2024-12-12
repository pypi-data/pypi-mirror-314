"""
Module related to work tasks
"""


class Task:
    def __init__(self, name: str, func, depends: list = []) -> None:
        """
        A computation, defined by a function, that can have dependencies
        """

        self.name = name
        self.func = func
        self.depends = depends

    def launch(self):
        self.func()
