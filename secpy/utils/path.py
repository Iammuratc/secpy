from pathlib import Path

def get_project_dir():
    """
    Get the project dir.
    Returns
    -------
    project_dir : Path
        <your-path-to-secpy>
    """
    project_dir = Path(__file__).resolve(strict=True).parent.parent.parent
    return project_dir


def create_dir(dir):
    """
    Create the given dir
    Parameters
    ----------
    dir : Path
        This dir path will be created if the user confirms it.
    Returns
    -------
    bool
    True if dir is confirmed to be created or if it already exists. Else, False.
    """
    if not dir.exists():
        msg = f'The following dir will be created:\n{dir}\nDo you confirm?[y/n] '
        ans = input(msg)
        if ans == 'y':
            Path(dir).mkdir(parents=True, exist_ok=True)
            return 1
        raise AssertionError('Please confirm it.\n')
    else:
        return 1