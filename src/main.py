import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Project sorting script")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
