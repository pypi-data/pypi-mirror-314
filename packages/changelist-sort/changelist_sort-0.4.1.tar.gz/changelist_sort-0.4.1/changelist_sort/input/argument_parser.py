"""Defines and Validates Argument Syntax.

Encapsulates Argument Parser.

Returns Argument Data, the args provided by the User.
"""
from argparse import ArgumentParser
from sys import exit

from changelist_sort.input.argument_data import ArgumentData
from changelist_sort.input.string_validation import validate_name


def parse_arguments(arguments: list[str] | None = None) -> ArgumentData:
    """ Parse command line arguments.

    Parameters:
    - args: A list of argument strings.

    Returns:
    ArgumentData : Container for Valid Argument Data.
    """
    if arguments is None or len(arguments) == 0:
        return ArgumentData()
    # Initialize the Parser and Parse Immediately
    try:
        return _validate_arguments(_define_arguments().parse_args(arguments))
    except SystemExit:
        exit("Unable to Parse Arguments.")


def _validate_arguments(
    parsed_args,
) -> ArgumentData:
    """ Checks the values received from the ArgParser.
        Uses Validate Name method from StringValidation.

    Parameters:
    - parsed_args : The object returned by ArgumentParser.

    Returns:
    ArgumentData - A DataClass of syntactically correct arguments.
    """
    if (cl_file := parsed_args.changelists_file) is not None:
        if not validate_name(cl_file):
            exit("Invalid Changelists File Name")
    if (ws_file := parsed_args.workspace_file) is not None:
        if not validate_name(ws_file):
            exit("Invalid Workspace File Name")
    return ArgumentData(
        changelists_path=cl_file,
        workspace_path=ws_file,
        sourceset_sort=parsed_args.sourceset_sort,
        remove_empty=parsed_args.remove_empty,
    )


def _define_arguments() -> ArgumentParser:
    """
    Initializes and Defines Argument Parser.
       - Sets Required/Optional Arguments and Flags.

    Returns:
    argparse.ArgumentParser - An instance with all supported Arguments.
    """
    parser = ArgumentParser(
        description="Changelist Sort",
    )
    # Optional Arguments
    parser.add_argument(
        '--changelists_file',
        type=str,
        default=None,
        help='The Changelists Data File. Searches default location if not provided.'
    )
    parser.add_argument(
        '--workspace_file', '--workspace',
        type=str,
        default=None,
        help='The Workspace File containing the ChangeList data. Searches default location if not provided.'
    )
    parser.add_argument(
        '-s', '--sourceset_sort', '--sourceset-sort',
        action='store_true',
        default=False,
        help='A Flag indicating that SourceSet Sort is to be used primarily. Fallback to Module Sort.',
    )
    parser.add_argument(
        '-r', '--remove_empty', '--remove-empty',
        action='store_true',
        default=False,
        help='A Flag indicating that empty changelists are to be removed after sorting.',
    )
    return parser
