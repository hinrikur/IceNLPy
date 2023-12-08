import argparse
from .iceparser import run_iceparser
from .icetagger import run_icetagger


def main():
    # Create the top-level parser
    parser = argparse.ArgumentParser(description="IceNLPy Command Line Interface")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create the parser for the "parser" command
    parser_parser = subparsers.add_parser("parser", help="Run IceParser")
    # Add arguments for the parser command if needed
    # parser_parser.add_argument('arg1', type=str, help='Description of arg1')

    # Create the parser for the "tagger" command
    tagger_parser = subparsers.add_parser("tagger", help="Run IceTagger")
    # Add arguments for the tagger command if needed
    # tagger_parser.add_argument('arg1', type=str, help='Description of arg1')

    # Parse the arguments
    args = parser.parse_args()

    if args.command == "parser":
        # Call function to run IceParser
        # Modify this line to pass any necessary arguments from args
        pass
    elif args.command == "tagger":
        # Call function to run IceTagger
        # Modify this line to pass any necessary arguments from args
        pass


if __name__ == "__main__":
    main()
