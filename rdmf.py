import shutil
import os


def get_project_path():
    """
    Prompt the user for confirmation to start from the current working directory.

    Returns:
        bool: True if the user confirms, False otherwise.
    """
    choice = input(
        "Are you sure you want to start from your current working directory? (y/n): ").title()
    return choice.lower() == "y"


def confirm_deletions(cwd):
    """
    Prompt the user for confirmation to delete a file or directory.

    Args:
        cwd (str): The current working directory.

    Returns:
        bool: True if the user confirms, False otherwise.
    """
    print(f'\n[*] {cwd}\n')
    choice = input(
        "Are you sure you want to delete the file or directory? (y/n): ").title()
    return choice.lower() == "y"


def is_dir_empty(directory):
    """
    Check if a directory is empty.

    Args:
        directory (str): The path to the directory.

    Returns:
        bool: True if the directory is empty, False otherwise.
    """
    return not any(os.scandir(directory))


def refresh_django_migrations_folders(cwd):
    """
    Delete a file or an empty directory.

    Args:
        entry (os.DirEntry): The file or directory entry to delete.
        sub_tap (str): The indentation string for subdirectories.
    """
    if os.path.isdir(cwd):
        for entry in os.scandir(cwd):
            if entry.name == "migrations" and entry.is_dir() and not is_dir_empty(entry.path):
                parent_dir = os.path.basename(os.path.dirname(entry.path))
                print(f"\n[*] {parent_dir} App:")
                for subentry in os.scandir(entry.path):
                    delete_entry(subentry)
                print("\n")
            elif entry.is_dir():
                refresh_django_migrations_folders(entry.path)


def is_dir_empty(directory):
    """
    Check if a directory is empty.

    Args:
        directory (str): The path to the directory.

    Returns:
        bool: True if the directory is empty, False otherwise.
    """
    return not any(os.scandir(directory))


def delete_entry(entry, sub_tap=''):
    """
    Delete a file or a directory (empty or non-empty), excluding folders containing __init__.py.

    Args:
        entry (os.DirEntry): The file or directory entry to delete.
        sub_tap (str): The indentation for printing.
    """
    try:
        if entry.is_dir():
            if not is_dir_empty(entry.path):
                sub_tap = '\t'
                has_init = False
                for subentry in os.scandir(entry.path):
                    if subentry.name == "__init__.py" and subentry.is_file():
                        has_init = True
                    else:
                        delete_entry(subentry, sub_tap)
                if has_init:
                    print(
                        f'\n\t{sub_tap}[+] Can\'t be Deleted __init__.py --- {entry.path}\n')
                else:
                    shutil.rmtree(entry.path)
                    print(f'\t{sub_tap}Deleted Directory {entry.path}')
            else:
                os.rmdir(entry.path)
                print(f'\t{sub_tap}Deleted Directory {entry.path}')

        elif entry.is_file() and entry.name != "__init__.py":
            os.remove(entry.path)
            print(f'\t{sub_tap}Deleted File --- {entry.path}')
        else:
            print(
                f'\n\t{sub_tap}[+] Can\'t be Deleted __init__.py --- {entry.path}\n')
    except Exception as e:
        raise e


if __name__ == '__main__':
    cwd = os.getcwd()
    path = get_project_path()
    if confirm_deletions(cwd):
        refresh_django_migrations_folders(cwd)
        print("Deletion completed successfully.")
