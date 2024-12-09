""" List Keys Definitions.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ListKey:
    """
    A Changelist Name and Key.

    Parameters:
    - key (str): The key used to quickly search for the changelist.
    - changelist_name (str): The full user defined name for the changelist.
    """
    key: str
    changelist_name: str


def compute_key(cl_name: str) -> ListKey:
    """
    Compute a Key to use for a given Changelist Name.
    - computation is a sequence of reduction operations

    Parameters:
    - cl_name (str): The Changelist Name to be included in the ListKey.

    Returns:
    ListKey - A ListKey instance containing the Key and Changelist Name.
    """
    if len(cl_name) == 0:
        return ListKey('', '')
    translator = str.maketrans('', '', ' :/\\')
    words = cl_name.translate(translator).split()
    return ListKey(
        key=''.join(w.lower() for w in words),
        changelist_name=cl_name
    )
