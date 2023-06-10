from rest_migrations.rm import _ProjectManager
import logging


class ProjectRunner:
    def __init__(self, pm):
        self.pm = pm
        self.cwd = None

    def _get_project_path(self):
        self.cwd = self.pm.get_user_choice()
        return self.cwd

    def _confirm_deletions(self):
        return self.pm.confirm_deletions()

    def _run_code(self):
        if self.cwd and self._confirm_deletions():
            self.pm.rest_migrations(self.cwd)

    @staticmethod
    def run():
        logging.basicConfig(level=logging.INFO,
                            format='%(levelname)s:rest_migrations:%(message)s')
        pm = _ProjectManager()
        runner = ProjectRunner(pm)
        runner._get_project_path()
        runner._run_code()
        if pm.success:
            success_msg = "Deletion completed successfully.\n" \
                "You can now recreate your migrations by running:\n" \
                "\tpython manage.py makemigrations\n" \
                "\tpython manage.py migrate"
            logging.info(success_msg)
        else:
            logging.warning(
                f"The directory {runner.cwd} does not contain any folder named 'migrations'.")
