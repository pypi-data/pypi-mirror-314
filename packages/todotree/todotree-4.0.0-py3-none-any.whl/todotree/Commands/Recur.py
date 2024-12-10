
from todotree.Commands.AbstractCommand import AbstractCommand
from todotree.Errors.RecurParseError import RecurParseError
from todotree.Managers.RecurManager import RecurManager


class Recur(AbstractCommand):

    def run(self):
        if not self.config.paths.recur_file.exists():
            self.config.console.error("recur.txt not found, nothing to add.")
            self.config.console.error("It should be at the following location:")
            self.config.console.error(self.config.paths.recur_file)
            exit(1)
        try:
            self()
        except RecurParseError as e:
            self.config.console.error(str(e))
            exit(1)
        self.config.git.commit_and_push("recur")

    def __call__(self, *args, **kwargs):
        rm = RecurManager(self.config)
        rm.import_tasks()
        rm.add_to_todo()
        rm._set_last_time_run()
