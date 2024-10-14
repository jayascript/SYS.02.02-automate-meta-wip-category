import argparse
import sys


def main():
    """
    Main entry point for the project sorting script.

    This function sets up the command-line interface using argparse,
    processes the provided arguments, and executes the appropriate actions
    based on those arguments.

    Command-line Arguments:
    --sort : Flag to initiate the project sorting process

    Usage:
    python3 main.py --sort  : Sort the projects
    python3 main.py --help  : Display help message

    Returns:
    None

    Raises:
    SystemExit: If no arguments are provided, exists with status code 1
                after displaying the help message.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Project sorting script - Organizes and prioritizes projects based on various criteria.",
        epilog="For more information, please refer to the project documentation."
    )

    # Add arguments
    parser.add_argument('--sort', action='store_true',
                        help="Sort the projects based on predefined criteria")

    # Parse arguments
    args = parser.parse_args()

    # Process arguments
    if args.sort:
        print("Sorting projects") # Placeholder for actual sorting logic
    elif len(sys.argv) == 1:
        # If no arguments are provided, print help message and exit
        parser.print_help(sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
