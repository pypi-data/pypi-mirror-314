"""
Atlas-Man CLI - A Command Line Interface to manage Trello and Jira projects.
"""

import argparse
from typing import Tuple, List
from atlasman.config import edit_config, load_config
from atlasman.trello_commands import TrelloCommands
from atlasman.jira_commands import JiraCommands

def add_trello_arguments(parser: argparse.ArgumentParser) -> None:
    """
    Add arguments specific to Trello commands.

    Args:
        parser (argparse.ArgumentParser):
            The argument parser to which Trello arguments will be added.
    """
    parser.add_argument(
        "--trello",
        "--t",
        help="Use Trello commands",
        action="store_true"
    )

    # Trello actions
    trello_actions = parser.add_argument_group('Trello Actions')
    trello_actions.add_argument(
        "--boards",
        action="store_true",
        help="List all Trello boards"
    )
    trello_actions.add_argument(
        "--lists",
        metavar="BOARD_NAME",
        type=str,
        help="List all Trello lists for a specified board"
    )
    trello_actions.add_argument(
        "--cards",
        metavar="LIST_ID",
        type=str,
        help="List all cards for a specified list by list ID"
    )
    trello_actions.add_argument(
        "--add-board",
        metavar="BOARD_NAME",
        type=str,
        help="Create a new Trello board"
    )
    trello_actions.add_argument(
        "--add-list",
        metavar=("BOARD_NAME", "LIST_NAME"),
        nargs=2,
        help="Create a new Trello list in a specified board"
    )
    trello_actions.add_argument(
        "--add-card",
        metavar=("LIST_NAME", "CARD_NAME"),
        nargs=2,
        help="Create a new Trello card in a specified list"
    )
    trello_actions.add_argument(
        "--update-board",
        metavar=("BOARD_ID", "NEW_NAME"),
        nargs=2,
        help="Update a Trello board"
    )
    trello_actions.add_argument(
        "--update-list",
        metavar=("LIST_ID", "NEW_NAME"),
        nargs=2,
        help="Update a Trello list"
    )
    trello_actions.add_argument(
        "--update-card",
        metavar=("CARD_ID", "NEW_NAME", "[DESCRIPTION]"),
        nargs='+',
        help="Update a Trello card. DESCRIPTION is optional."
    )
    trello_actions.add_argument(
        "--delete-board",
        metavar="BOARD_NAME",
        type=str,
        help="Delete a Trello board"
    )
    trello_actions.add_argument(
        "--delete-list",
        metavar="LIST_NAME",
        type=str,
        help="Delete a Trello list from a specified board"
    )
    trello_actions.add_argument(
        "--delete-card",
        metavar="CARD_NAME",
        type=str,
        help="Delete a Trello card from a specified list"
    )


def add_jira_arguments(parser: argparse.ArgumentParser) -> None:
    """
    Add arguments specific to Jira commands.

    Args:
        parser (argparse.ArgumentParser): The argument parser to which Jira arguments will be added.
    """
    parser.add_argument(
        "--jira",
        "--j",
        help="Use Jira commands",
        action="store_true"
    )

    # Jira actions
    jira_actions = parser.add_argument_group('Jira Actions')
    jira_actions.add_argument(
        "--issues",
        metavar="PROJECT_KEY",
        type=str,
        nargs="?",
        const="default",
        help="List all Jira issues for a specified project. \
If no project is provided, uses default."
    )
    jira_actions.add_argument(
        "--projects",
        action="store_true",
        help="List all Jira projects"
    )
    jira_actions.add_argument(
        "--add-issue",
        metavar=("PROJECT_KEY", "ISSUE_TITLE"),
        nargs="+",
        help="Add a new Jira issue."
    )
    jira_actions.add_argument(
        "--update-issue",
        metavar=("ISSUE_ID", "NEW_TITLE"),
        nargs=2,
        type=str,
        help="Update an existing Jira issue"
    )
    jira_actions.add_argument(
        "--delete-issue",
        metavar="ISSUE_ID",
        type=str,
        help="Delete a Jira issue by issue ID"
    )
    jira_actions.add_argument(
        "--add-project",
        metavar=("PROJECT_NAME", "PROJECT_KEY"),
        nargs=2,
        type=str,
        help="Create a new Jira project"
    )
    jira_actions.add_argument(
        "--delete-project",
        metavar="PROJECT_KEY",
        type=str,
        help="Delete a Jira project by project key"
    )
    jira_actions.add_argument(
        "--type",
        "--issue-type",
        metavar="ISSUE_TYPE",
        type=str,
        help="Specify the issue type for a new Jira issue"
    )


def parse_arguments() -> argparse.Namespace:
    """
    Add command-line arguments for Atlas-Man.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="A CLI to manage Trello and Jira projects")

    # Add Trello and Jira arguments
    add_trello_arguments(parser)
    add_jira_arguments(parser)

    return parser.parse_args()

def validate_arguments(args: argparse.Namespace,
                    remaining_args: List[str],
                    trello_commands: TrelloCommands,
                    jira_commands: JiraCommands) -> Tuple[argparse.Namespace, List[str]]:
    """
    Validate arguments based on Trello or Jira context and return parsed arguments and any unknowns.

    Args:
        args (argparse.Namespace): Parsed arguments from the initial context check.
        remaining_args (List[str]): Remaining arguments to be parsed in context.

    Returns:
        Tuple[argparse.Namespace, List[str]]:
            Parsed context-specific arguments and any unrecognized arguments.
    """
    if args.trello:
        # Parse Trello-specific commands
        trello_parser = argparse.ArgumentParser(description="Trello-specific commands")
        add_trello_arguments(trello_parser)
        trello_args, unknown = trello_parser.parse_known_args(remaining_args)

        # handle empty arguments
        if all(not value for value in vars(trello_args).values()):
            print("Remaining args before parsing:", remaining_args)
            trello_parser.print_help()
            return trello_args, unknown

        if unknown:
            print(f"Error: Unrecognized arguments for Trello: {' '.join(unknown)}")
            trello_parser.print_help()
            return trello_args, unknown

        try:
            trello_commands.handle_trello_commands(trello_args)
        except TypeError as e:
            print(f"Error: {str(e)}")
            trello_parser.print_help()
            return trello_args, []
        return trello_args, []

    elif args.jira:
        # Parse Jira-specific commands
        jira_parser = argparse.ArgumentParser(description="Jira-specific commands")
        add_jira_arguments(jira_parser)
        jira_args, unknown = jira_parser.parse_known_args(remaining_args)

        # handle empty arguments
        if all(not value for value in vars(jira_args).values()):
            jira_parser.print_help()
            return jira_args, unknown

        if unknown:
            print(f"Error: Unrecognized arguments for Jira: {' '.join(unknown)}")
            jira_parser.print_help()
            return jira_args, unknown

        try:
            jira_commands.handle_jira_commands(jira_args)
        except TypeError as e:
            print(f"Error: {str(e)}")
            jira_parser.print_help()
            return jira_args, []
        return jira_args, []

    elif args.config:
        # Edit the configuration file in the default editor
        edit_config()

        return args, remaining_args

    else:
        # print help if no context is provided
        raise argparse.ArgumentError(argument=None,
                                     message="No arguments provided.")

def main() -> None:
    """
    The main function that serves as the entry point for the CLI.
    """
    try:
        # Initial parser to identify the command context
        parser = argparse.ArgumentParser(description="A CLI to manage Trello and Jira projects")
        parser.add_argument("--trello", "--t", help="Use Trello commands", action="store_true")
        parser.add_argument("--jira", "--j", help="Use Jira commands", action="store_true")
        parser.add_argument("--config", help="Edit the configuration file", action="store_true")

        # Parse initial command context
        args, remaining_args = parser.parse_known_args()

        # Load configuration and pass necessary values to command handlers
        config = load_config()
        cli_config = config.get("cli", {})

        # Set verbosity if specified in config
        verbose = cli_config.get("verbose", False)
        if verbose:
            print("Running in verbose mode...")

        # Initialize TrelloCommands and JiraCommands
        trello_commands = TrelloCommands(config)
        jira_commands = JiraCommands(config)

        # Validate arguments based on context and handle commands
        validated_args = validate_arguments(args, remaining_args, trello_commands, jira_commands)

        if not validated_args:
            parser.print_help()

    except (argparse.ArgumentError, TypeError) as e:
        print(f"Parsing Error: {str(e)}")
        if args.trello:
            print("Please check the Trello-specific syntax in README.md.\n")
        elif args.jira:
            print("Please check the Jira-specific syntax in README.md.\n")
        parser.print_help()
    except Exception as e: # pylint: disable=broad-except
        print(f"An unexpected error occurred: {str(e)}")
        raise
    except KeyboardInterrupt:
        print("\n\nCanceled.")

if __name__ == "__main__":
    main()
