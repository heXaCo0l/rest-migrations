import logging
import shutil
import os


class _ProjectManager:
    def __init__(self) -> None:
        self.success = False

    def get_user_choice(self):
        options = "[1] Clear all migrations folders in this working directory\n" \
            "[2] Provide a path to clear migrations folders\n" \

        logging.warning(
            "----- Make sure you have a backup for your folders -----")

        choice = input("Options:\n" + options + "Enter your choice: ").strip()
        if choice.lower() == "1":
            cwd = os.getcwd()
            logging.info(f"[*] {cwd}")
            return cwd
        elif choice.lower() == "2":
            folder_path = input("Provide the folder path: ").strip()
            if os.path.isdir(folder_path):
                if not self.is_dir_empty(folder_path):
                    logging.info(f"[*] {folder_path}")
                    return folder_path
                else:
                    logging.warning("The folder is empty.")
            else:
                logging.warning("The path is not a folder.")
        else:
            os._exit(0)

    def confirm_deletions(self):
        """
        Prompt the user for confirmation to delete a file or directory.

        Returns:
            bool: True if the user confirms, False otherwise.
        """
        choice = input(
            "Are you sure you want to continue with this path? (y/n): ").title()
        return choice.lower() == "y"

    def is_dir_empty(self, directory):
        """
        Check if a directory is empty.

        Args:
            directory (str): The path to the directory.

        Returns:
            bool: True if the directory is empty, False otherwise.
        """
        return not any(os.scandir(directory))

    def rest_migrations(self, cwd):
        """
        Delete a file or an empty directory.

        Args:
            cwd (str): The current working directory.
        """
        if os.path.isdir(cwd):
            for entry in os.scandir(cwd):
                if entry.name == "migrations" and entry.is_dir() and not self.is_dir_empty(entry.path):
                    self.success = True
                    parent_dir = os.path.basename(os.path.dirname(entry.path))
                    logging.info(f"[*] {parent_dir} App:")
                    for subentry in os.scandir(entry.path):
                        self.delete_entry(subentry)
                    logging.info("")
                elif entry.is_dir():
                    self.rest_migrations(entry.path)

    def delete_entry(self, entry, sub_tap=''):
        """
        Delete a file or a directory (empty or non-empty), excluding folders containing __init__.py.

        Args:
            entry (os.DirEntry): The file or directory entry to delete.
            sub_tap (str): The indentation for printing.
        """
        try:
            if entry.is_dir():
                if not self.is_dir_empty(entry.path):
                    sub_tap = '\t'
                    has_init = False
                    for subentry in os.scandir(entry.path):
                        if subentry.name == "__init__.py" and subentry.is_file():
                            has_init = True
                        else:
                            self.delete_entry(subentry, sub_tap)
                    if has_init:
                        logging.info(
                            f"\n\t{sub_tap}[+] Can't be Deleted __init__.py --- {entry.path}\n")
                    else:
                        shutil.rmtree(entry.path)
                        logging.info(
                            f"\t{sub_tap}Deleted Directory {entry.path}")
                else:
                    os.rmdir(entry.path)
                    logging.info(f"\t{sub_tap}Deleted Directory {entry.path}")
            elif entry.is_file() and entry.name != "__init__.py":
                os.remove(entry.path)
                logging.info(f"\t{sub_tap}Deleted File --- {entry.path}")
            else:
                logging.info(
                    f"\n\t{sub_tap}[+] Can't be Deleted __init__.py --- {entry.path}\n")
        except Exception as e:
            raise e
