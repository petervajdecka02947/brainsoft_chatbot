import argparse
from cli_commands import setup_cli


def main():
    parser = argparse.ArgumentParser(description="CLI for FastAPI backend interaction")
    setup_cli(parser)
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
