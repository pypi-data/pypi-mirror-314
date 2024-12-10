import importlib

from todotree.Commands.AbstractCommand import AbstractCommand


class Version(AbstractCommand):

    def run(self):
        version = importlib.metadata.version("todotree")
        if self.config.console.is_verbose():
            self.config.console.verbose(f"The version is {version}")
        elif self.config.console.is_quiet():
            self.config.console.warning(version)
        else:
            self.config.console.info(f"Version: {version}")

    def __call__(self, *args, **kwargs):
        NotImplemented