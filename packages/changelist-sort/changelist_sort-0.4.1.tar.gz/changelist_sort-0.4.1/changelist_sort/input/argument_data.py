"""The Arguments Received from the Command Line Input.

This DataClass is created after the argument syntax is validated.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ArgumentData:
    """
    The syntactically valid arguments recevied by the Program.

    Fields:
    - changelists_path (str | None): The path to the Changelists file, or None to enable defaults.
    - workspace_path (str | None): The path to the workspace file, or None to enable defaults.
    - sourceset_sort (bool): Flag for the SourceSet SortMode.
    - remove_empty (bool): Flag indicating that empty changelists should be removed.
    """
    changelists_path: str | None = None
    workspace_path: str | None = None
    sourceset_sort: bool = False
    remove_empty: bool = False
