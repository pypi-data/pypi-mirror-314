import re
import subprocess

from todotree.Commands.AbstractCommand import AbstractCommand
from todotree.Errors.TodoFileNotFoundError import TodoFileNotFoundError
from todotree.Task.Task import Task


class Schedule(AbstractCommand):
    def run(self, new_date=None, task_number=None):
        # Disable fancy imports, because they do not have t dates.
        self.config.enable_project_folder = False
        # Convert
        date = " ".join(new_date)
        date_pattern = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
        if not date_pattern.match(date):
            self.config.console.verbose(f"Attempt to parse {date} with the `date` program.")
            # Try to use the `date` utility.
            dat = subprocess.run(
                ["date", "-d " + date, "+%F "],
                capture_output=True,
                encoding="utf-8"
            )
            if dat.returncode > 0:
                self.config.console.error(f"The date {new_date} could not be parsed.")
                exit(1)
            date = dat.stdout.strip()
        try:
            self.taskManager.import_tasks()
            self.config.console.info(f"Task {task_number} hidden until {date}")
            updated_task = self.taskManager.add_or_update_task(task_number, Task.add_or_update_t_date, date)
            self.config.console.info(str(updated_task))
        except TodoFileNotFoundError as e:
            e.echo_and_exit(self.config)
        self.config.git.commit_and_push("schedule")

    def __call__(self, *args, **kwargs):
        NotImplemented