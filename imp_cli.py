import argparse
from processing.postproc import (
    create_input_folder,
    remove_linebrakes,
)


def cmd_post_init(args):
    create_input_folder(args.directory)


def cmd_post(args):
    remove_linebrakes(in_path=args.directory)


def main():
    parser = argparse.ArgumentParser(
        description="A CLI tool for processing images for OCR"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # post init parser
    post_parser = subparsers.add_parser(
        "post_init", help="Initialise directory for post-processing."
    )
    post_parser.add_argument(
        "directory",
        nargs="?",
        default="postp_input",
        help="Post-processing input directory name. Defaults to 'postp_input'",
    )
    post_parser.set_defaults(func=cmd_post_init)

    # post parser
    post_parser = subparsers.add_parser("post", help="Post-processing.")
    post_parser.add_argument(
        "directory",
        nargs="?",
        default=None,
        help="Optional input directory for post-processing",
    )
    post_parser.set_defaults(func=cmd_post)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
