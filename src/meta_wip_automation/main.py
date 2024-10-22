import argparse
import sys
from typing import List
from meta_wip_automation.project_sorter import sort_projects
from meta_wip_automation.readme_parser import parse_readme, extract_frontmatter
from datetime import datetime


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
        description="Project sorting script for neurodivergent-friendly task management.",
        epilog="For more information, please refer to the project documentation."
    )

    # Add arguments
    parser.add_argument('--sort', nargs='+', metavar='FILE',
                        help="Sort the projects based on predefined criteria")

    # Parse arguments
    args = parser.parse_args()

    if args.sort:
        # Process each README file
        projects = []
        for file_path in args.sort:
            try:
                content = parse_readme(file_path)
                frontmatter = extract_frontmatter(content)

                # Check if frontmatter is valid
                if not frontmatter or 'title' not in frontmatter:
                    raise ValueError("Invalid or missing frontmatter")

                # Handle recurence if specified
                last_completed = None
                recurrence_interval = None
                if 'RECURRENCE_INTERVAL' in frontmatter and 'LAST_COMPLETED' in frontmatter:
                    recurrence_interval = int(frontmatter['RECURRENCE_INTERVAL'])
                    last_completed = datetime.strptime(frontmatter['LAST_COMPLETED'], '%Y-%m-%d')

                projects.append((frontmatter, last_completed, recurrence_interval))
            except FileNotFoundError as e:
                print(f"Error processing {file_path}: {str(e)}", file=sys.stderr)
                continue
            except Exception as e:
                print(f"Error processing {file_path}: Invalid frontmatter format", file=sys.stderr)
                continue

        if projects: # Only sort and display results if we have valid README files
            sorted_projects = sort_projects(projects)
            print("\nProjects in priority order:")
            print("-" * 40)
            for i, (frontmatter, _, _) in enumerate(sorted_projects, 1):
                print(f"{i}. {frontmatter.get('title', 'Untitled')} ({frontmatter.get('PROJECT_ID', 'No ID')})")
                print(f"   Status: {frontmatter.get('STATUS', 'unknown')}")
                print(f"   Urgency: {frontmatter.get('URGENCY', 'unknown')}")
                print()
    elif len(sys.argv) == 1:
        # If no arguments are provided, print help message and exit
        parser.print_help(sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
