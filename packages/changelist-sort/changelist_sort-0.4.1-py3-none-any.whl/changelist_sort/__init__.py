""" Main Package Methods.
"""
from changelist_data.changelist import Changelist

from changelist_sort.changelist_data import ChangelistData, simplify, expand
from changelist_sort.sorting import sort
from changelist_sort.input.input_data import InputData


def sort_changelists(
    input_data: InputData,
):
    """ Sort the given Changelists and write them to the Workspace File.
    """
    sorted_lists = sort(
        expand_changelists(
            input_data.storage.get_changelists()
        ),
        input_data.sort_mode,
        input_data.sorting_config
    )
    if input_data.remove_empty: # Filter out Empty Changelists
        sorted_lists = list(filter(
            lambda x: len(x.changes) > 0,
            sorted_lists
        ))
    input_data.storage.update_changelists(
        simplify_changelists(
            sorted_lists
        )
    )
    input_data.storage.write_to_storage()


def simplify_changelists(
    data: list[ChangelistData]
) -> list[Changelist]:
    return [ simplify(x) for x in data ]


def expand_changelists(
    data: list[Changelist]
) -> list[ChangelistData]:
    return [ expand(x) for x in data ]
