import argparse
from . import icetagger, iceparser, tokenizer


def run_tokenizer(input_text, *args, **kwargs) -> str:
    # Placeholder function for tokenizer functionality
    print(kwargs)
    tokenized = tokenizer.tokenize(input_text)
    sent_sep = "\n" if kwargs.get("output_format") == 1 else "\n\n"
    token_sep = "\n" if kwargs.get("output_format") == 1 else " "
    return sent_sep.join([token_sep.join(sentence) for sentence in tokenized])


def run_tagger(input_text, *args, **kwargs):
    # Placeholder function for tagger functionality
    return icetagger.tag_text([input_text])


def run_parser(input_text, *args, **kwargs):
    # Placeholder function for parser functionality
    parsed = iceparser.parse_text([input_text], legacy_tagger=True)
    if kwargs.get("tree_view"):
        return "\n".join([sent.view for sent in parsed])
    return parsed


def setup_cli():
    parser = argparse.ArgumentParser(description="IceNLPy Command Line Interface")
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Available commands"
    )

    # Setup tokenizer command
    tokenizer_parser = subparsers.add_parser(
        "tokenizer", help="Run Tokenizer on the input text"
    )
    add_common_arguments(tokenizer_parser)

    # Setup tagger command
    tagger_parser = subparsers.add_parser(
        "icetagger", help="Run IceTagger. Tokenizes and tags the input text."
    )
    add_common_arguments(tagger_parser)

    # Setup parser command
    parser_parser = subparsers.add_parser(
        "iceparser", help="Run IceParser. Tokenizes, tags, and parses the input text."
    )
    add_common_arguments(parser_parser)

    return parser


def add_common_arguments(subparser):
    subparser.add_argument("-i", "--input", type=str, help="Input file path")
    subparser.add_argument("-o", "--output", type=str, help="Output file path")
    subparser.add_argument("input_text", nargs="?", help="Direct text to process")
    subparser.add_argument(
        "-of",
        "--output-format",
        type=int,
        default=2,
        help="The desired output format. 1 for one token per line, 2 for one sentence per line.",
        choices=[1, 2],
    )

    subparser.add_argument(
        "-t",
        "--tree-view",
        action="store_true",
        help="Print the output in a tree view format. Only applies to IceParser.",
    )


def process_input_output(args):
    input_text = args.input_text

    operations = {
        "tokenizer": run_tokenizer,
        "icetagger": run_tagger,
        "iceparser": run_parser,
    }

    if args.input:
        with open(args.input, "r") as file:
            input_text = file.read()

    output_text = operations[args.command](**vars(args))

    if args.output:
        with open(args.output, "w") as file:
            file.write(output_text)
    else:
        print(output_text)


def main():
    cli_parser = setup_cli()
    args = cli_parser.parse_args()

    if not args.command:
        cli_parser.print_help()
    else:
        process_input_output(args)


if __name__ == "__main__":
    main()
