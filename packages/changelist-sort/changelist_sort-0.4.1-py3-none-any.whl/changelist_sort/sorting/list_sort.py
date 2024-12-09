""" Changelist Sorting Methods.
"""
from typing import Callable

from changelist_sort.change_data import ChangeData
from changelist_sort.changelist_data import ChangelistData
from changelist_sort.list_key import ListKey


def split_changelist(
    changelist: ChangelistData,
    is_sorted: Callable[[ListKey, ChangeData], bool],
) -> list[ChangeData]:
    """
    Split the Changelist by checking that all changes are sorted.
        Removes each element that is returned from the changelist.

    Parameters:
    - changelist (ChangelistData): The Changelist to split based on sorting function.
    - is_sorted (callable[bool]): A Function that determines whether a Change is Sorted.

    Returns:
    list[ChangeData] - The List of ChangeData that are Unsorted, now removed from this changelist.
    """
    unsorted_files = []
    for index in range(len(changelist.changes) - 1, -1, -1):
        if not is_sorted(
            changelist.list_key,
            changelist.changes[index]
        ):
            unsorted_files.append(
                changelist.changes.pop(index)
            )
    return unsorted_files
