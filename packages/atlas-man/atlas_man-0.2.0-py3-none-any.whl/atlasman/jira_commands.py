"""
This module provides functions to interact with the Jira API.
"""

import argparse
import traceback
from typing import Any, Dict
from jira import Issue, JIRA, JIRAError
from tabulate import tabulate
from .constants.jira_field_types import JIRA_FIELD_TYPES

# Decorator to handle common Jira-related exceptions
def handle_jira_exceptions(func):
    """
    A decorator to handle common Jira-related exceptions.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except JIRAError as e:
            print(f"JIRA error: {e}")
        except ValueError as e:
            print(f"Value error: {e}")
        except Exception as e:  # pylint: disable=broad-except
            print(f"Unexpected error in {func.__qualname__}: {e}")
            traceback.print_exc()
    return wrapper


class JiraCommands:
    """
    The JiraCommands class provides functions to interact with the Jira API.
    """

    def __init__(self, config_data: Dict[str, Any]) -> None:
        """
        Initializes the JiraCommands class with the given configuration.

        Args:
            config_data (Dict[str, Any]):
                The configuration dictionary containing Jira API credentials.
        """

        self.config: Dict[str, Any] = config_data
        self.client: JIRA = self.initialize_jira_client()

    def initialize_jira_client(self) -> JIRA:
        """
        Initializes and returns a Jira client using credentials from the config.
        
        Returns:
            JIRA: An instance of the JIRA client configured with API credentials.
        """

        config_jira = self.config.get("jira", {})

        base_url = config_jira.get("base_url")
        username = config_jira.get("username")
        api_token = config_jira.get("api_token")

        # Validate presence of necessary credentials
        if not base_url or not username or not api_token:
            raise ValueError("Missing required Jira credentials ",
                             "(base_url, username, or api_token) in the configuration file.")

        # Initialize JIRA client with API token for basic auth
        return JIRA(server=base_url, basic_auth=(username, api_token))

    @handle_jira_exceptions
    def list_projects(self) -> None:
        """
        Lists all projects available in Jira.
        """
        projects = self.client.projects()
        for project in projects:
            print(f"Project Name: {project.name} - Project Key: {project.key}")

    @handle_jira_exceptions
    def list_issues(self, project_key: str) -> None:
        """
        Lists all issues for a specified project, sorted by status in a custom order.

        Args:
            project_key (str): The key of the project to list issues from.
        """

        print(f"Issues for {project_key}:")
        issues = self.client.search_issues(f'project="{project_key}"')

        # Custom order for statuses
        status_order = {
            "To Do": 1,
            "In Progress": 2,
            "Testing": 3,
            "Done": 4
        }

        # Check if the response is a ResultList of Issue objects
        if isinstance(issues, list) or hasattr(issues, 'total'):
            # Collect issues in a list with their statuses for sorting
            issue_list = []
            for issue in issues:
                if isinstance(issue, Issue):
                    if issue.fields.status.name == "Done" and \
                        not self.config["jira"]["show_done_issues"]:
                        continue
                    # Assign a sort index; default to 0 if not in the custom order
                    status_index = status_order.get(issue.fields.status.name, 0)
                    issue_list.append((status_index, issue.fields.status.name,
                                       issue.key, issue.fields.summary))
                else:
                    print(f"Unexpected item type in issues list: {type(issue)}")

            # Sort the issue list by the custom status index
            issue_list.sort(key=lambda x: x[0])

            # Create a table using tabulate
            table = tabulate(
                [(status, key, summary) for _, status, key, summary in issue_list],
                headers=["Status", "Issue Key", "Summary"],
                tablefmt="grid"
            )
            print(table)

        elif isinstance(issues, dict):
            print("Received response as dictionary. Inspecting keys for more details.")
            for key, value in issues.items():
                print(f"{key}: {value}")
        else:
            print("Unexpected issue format received from Jira API.")

    @handle_jira_exceptions
    def add_project(self, project_name: str, project_key: str) -> None:
        """
        Creates a new project with the specified name and key,
        allowing the user to choose a project type.
        
        Args:
            project_name (str): The name of the project to create.
            project_key (str): The key for the project to create.
        """
        # Prompt the user for project type
        project_type = input(
            "Select the type of project to create:\n"
            "(k) Kanban\n"
            "(s) Simplified project management\n"
            "(c) Scrum\n"
            "(b) Bug tracking\n"
            "Enter your choice (k/s/c/b): "
        ).strip().lower()

        # Determine the project template key based on user input
        if project_type == 'k':
            project_template_key = "com.pyxis.greenhopper.jira:gh-simplified-agility-kanban"
        elif project_type == 's':
            project_template_key = \
                "com.atlassian.jira-core-project-templates:jira-core-simplified-project-management"
        elif project_type == 'c':
            project_template_key = "com.pyxis.greenhopper.jira:gh-simplified-agility-scrum"
        elif project_type == 'b':
            project_template_key = \
                "com.atlassian.jira.jira-software-project-templates:jira-software-bug-tracking"
        else:
            print("Error: Invalid choice. Please enter 'k', 's', 'c', or 'b'.")
            return

        # Attempt to create the project with the selected template
        try:
            # Create the project and retrieve the project ID
            project_id = self.client.create_project(
                key=project_key,
                name=project_name,
                template_name=project_template_key,
            )

            if not project_id:
                print("Error: Project creation failed.")
                return

            # Safely access base URL
            base_url = self.config.get('jira', {}).get('base_url', "")
            if base_url:
                # Fetch the board associated with the new project
                boards = self.client.boards(projectKeyOrID=project_key)
                if boards:
                    # Assuming we take the first board if multiple are returned
                    board_id = boards[0].id
                    project_link = \
                        f"{base_url}/jira/software/projects/{project_key}/boards/{board_id}"
                    print(f"Project '{project_name}' created successfully with Key: {project_key}")
                    print(f"Project link: {project_link}")
                else:
                    print(f"Project '{project_name}' created successfully with Key: {project_key}")
                    print("Warning: No boards found for this project.")
            else:
                print(f"Project '{project_name}' created successfully with Key: {project_key}")
                print("Warning: Base URL is missing in the configuration,",
                      "so the project link could not be generated.")

        except JIRAError as e:
            if e.status_code == 400 and "issue security scheme" in e.text:
                print("Error: Unable to retrieve issue security scheme.",
                      "Please check your Jira configuration.")
            elif e.status_code == 403:
                print("Error: You do not have the required admin privileges to create projects.")
            else:
                raise  # Reraise other errors for the decorator to handle

    def add_issue(self, project_key: str, issue_title: str, issue_type: str = 'Task') -> None:
        """
        Adds a new issue to the specified project.

        Args:
            project_key (str): The key of the project where the issue will be added.
            issue_title (str): The title of the issue.
            issue_type (str): The type of the issue, e.g., "Story", "Task".
        """

        # Capitalize Issue Type
        default_issue_type: str = self.config["jira"].get("default_issue_type")
        if issue_type:
            issue_type = issue_type.lower().capitalize()
        elif default_issue_type:
            issue_type = default_issue_type
        else:
            issue_type = input("Enter an issue type: ").lower().capitalize()

        fields = {
            'project': {'key': project_key},
            'summary': issue_title,
            'issuetype': {'name': issue_type}
        }

        def _parse_fields(errors):
            """Handles required field errors by prompting the user for input."""

            def _prompt_for_field(field, message):
                """Prompts the user for a missing field based on its expected type."""
                expected_type = JIRA_FIELD_TYPES.get(field, str)

                # Prompt based on expected type
                if expected_type == int:
                    value = int(input(
                        f"Enter a number for {message.replace(' is required.', '')}: "))
                elif expected_type == list:
                    value = input(
                        f"Enter values for {message.replace(
                            ' is required.', '')} (comma-separated): ")
                    value = [item.strip() for item in value.split(',')]
                elif expected_type == dict:
                    if 'issuetype' in field:
                        # Special handling for issuetype fields if needed
                        value = input("Enter an issue type: ").lower().capitalize()
                    elif 'customfield_' in field:
                        data = self.client.createmeta(
                            projectKeys=project_key,
                            issuetypeNames=issue_type,
                            expand='projects.issuetypes.fields'
                        )
                        allowed_values = None
                        for project in data.get("projects", []):
                            for issuetype in project.get("issuetypes", []):
                                available_fields = issuetype.get("fields", {})
                                if field in available_fields:
                                    allowed_values = available_fields[field].get(
                                        "allowedValues", [])
                                    break  # Stop after finding the first instance

                        # Print or further process the allowed values for customfield
                        if allowed_values:
                            print("Enter an ID from the following:")
                            for option in allowed_values:
                                print(f"{option['id']} - {option['value']}")
                            value = {"id": input("\n")}
                else:
                    # Default case for str or any unexpected type
                    value = input(f"Enter {message.replace(' is required.', '')}: ")

                fields[field] = value

            # Process each error field using _prompt_for_field
            for field, message in errors.items():
                _prompt_for_field(field, message)

        try:
            new_issue = self.client.create_issue(fields=fields)
            print(f"{issue_type} '{new_issue.key}' created successfully in '{project_key}'.")
            print(f"{self.config["jira"]["base_url"]}/browse/{new_issue.key}")
        except JIRAError as e:
            if e.status_code == 400:
                errors = e.response.json().get('errors', {})
                _parse_fields(errors)  # Call the inner function to handle field parsing

                # Retry creating the issue with additional required fields
                new_issue = self.client.create_issue(fields=fields)
                print(f"{issue_type} '{new_issue.key}' created "
                    f"successfully in project '{project_key}'.")
            else:
                print(f"Failed to create issue: {e}")

    @handle_jira_exceptions
    def update_issue(self, issue_id: str, new_title: str) -> None:
        """
        Updates the title of an existing issue.

        Args:
            issue_id (str): The ID of the issue to update.
            new_title (str): The new title for the issue.
        """
        issue = self.client.issue(issue_id)
        issue.update(fields={"summary": new_title})
        print(f"Issue '{issue_id}' updated successfully.")

    @handle_jira_exceptions
    def delete_issue(self, issue_id: str) -> None:
        """
        Deletes an issue by its ID or numeric identifier, with a confirmation prompt requiring
        the user to re-enter the exact issue key.

        Args:
            issue_id (str): The ID or numeric part of the issue to delete.
        """
        try:
            # Normalize issue ID to handle either full key (e.g., 'ANT-123')
            # or numeric part (e.g., '123')
            if '-' not in issue_id:
                # Assume it's only the numeric part and prepend the project key, if needed
                project_key = self.config["jira"].get("default_project_key")
                issue_id = f"{project_key}-{issue_id}"

            # Fetch the issue using the normalized issue key
            issue = self.client.issue(issue_id)
            issue_key = issue.key  # Full issue key, e.g., 'ANT-123'
            issue_title = issue.fields.summary  # Get the issue title for context

            # Display warning and request exact confirmation
            print(f"Warning: You are about to delete the issue '{issue_title}' (Key: {issue_key}).")
            confirmation_text = ("This action is irreversible.\n"
                                 f"To confirm deletion, please enter the issue key '{issue_key}': ")
            confirmation = input(confirmation_text).strip()

            # Check if the entered key matches exactly
            if confirmation != issue_key:
                print("Deletion canceled: Issue key did not match exactly.")
                return

            # Proceed with deletion if confirmed
            issue.delete()
            print(f"Issue '{issue_key}' deleted successfully.")

        except JIRAError as e:
            if e.status_code == 403:
                print("Error: You do not have the required permissions to delete this issue.")
            elif e.status_code == 404:
                print(f"Error: Issue '{issue_id}' not found.")
            else:
                raise  # Reraise other errors for the decorator to handle

    @handle_jira_exceptions
    def delete_project(self, project_key: str) -> None:
        """
        Deletes a project by its key, with a confirmation prompt
        requiring the user to enter the project title.

        Args:
            project_key (str): The key of the project to delete.
        """
        try:
            # Fetch the project using the project key
            project = self.client.project(project_key)
            project_name = project.name  # Get the project title for confirmation

            # Display warning and request confirmation
            print("Warning: You are about to delete the project",
                  f"'{project_name}' (Key: {project_key}).")
            warning_text = ("This action is dangerous.\n"
                            f"To confirm deletion, please enter the title '{project_name}': ")
            confirmation = input(warning_text).strip()

            # Check if the entered title matches (case-insensitive)
            if confirmation.lower() != project_name.lower():
                print("Deletion canceled: Project title did not match.")
                return

            # Proceed with deletion if confirmed
            project.delete()
            print(f"Project '{project_key}' deleted successfully.")

        except JIRAError as e:
            if e.status_code == 403:
                print("Error: You do not have the required admin privileges to delete projects.")
            elif e.status_code == 404:
                print(f"Error: Project '{project_key}' not found.")
            else:
                raise  # Reraise other errors for the decorator to handle

    def handle_jira_commands(self, args: argparse.Namespace) -> None:
        """
        Handle Jira commands based on the provided arguments.

        Args:
            args (argparse.Namespace): The parsed command-line arguments.
        """

        if args.issues:
            # Use the default project if no specific project key is provided
            if args.issues == "default":
                project_key = self.config["jira"].get("default_project_key")
            else:
                project_key = args.issues
            if project_key:
                self.list_issues(project_key)
            else:
                print("Error: No project key provided,",
                      "and no default project set in configuration.")
        elif args.projects:
            self.list_projects()
        elif args.add_issue:
            # Check if one or two arguments were provided for --add-issue
            if len(args.add_issue) == 1:
                # Use default project and provided title
                project_key = self.config["jira"].get("default_project_key")
                issue_title = args.add_issue[0]
            elif len(args.add_issue) < 3:
                # Use provided project key and title
                project_key = args.add_issue[0]
                issue_title = args.add_issue[1]
            else:
                raise TypeError("Invalid number of arguments for --add-issue.\n")

            # Ensure project key is available before proceeding
            if project_key:
                self.add_issue(project_key, issue_title, issue_type=args.type)
            else:
                print("Error: No project key provided,",
                      "and no default project set in configuration.")
        elif args.update_issue:
            self.update_issue(args.update_issue[0], args.update_issue[1])
        elif args.delete_issue:
            self.delete_issue(args.delete_issue)
        elif args.add_project:
            self.add_project(args.add_project[0], args.add_project[1])
        elif args.delete_project:
            self.delete_project(args.delete_project)
