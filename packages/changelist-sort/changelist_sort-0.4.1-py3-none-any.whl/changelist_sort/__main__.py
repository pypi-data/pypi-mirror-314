#!/usr/bin/python
from sys import argv, path


def main():
    from changelist_sort.input import validate_input
    from changelist_sort import sort_changelists
    input_data = validate_input(argv[1:])
    sort_changelists(input_data)
    #print(output_data)


if __name__ == "__main__":
    from pathlib import Path
    # Get the directory of the current file (__file__ is the path to the script being executed)
    current_directory = Path(__file__).resolve().parent.parent
    # Add the directory to sys.path
    path.append(str(current_directory))
    main()
