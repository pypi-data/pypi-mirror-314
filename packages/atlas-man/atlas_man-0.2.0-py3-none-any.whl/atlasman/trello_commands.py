"""
This module provides functions to interact with the Trello API.
"""

import os
import argparse
import traceback
from typing import Any, Dict
from trello import TrelloClient
from trello import TokenError
from trello.exceptions import ResourceUnavailable

# Decorator to handle common Trello-related exceptions
def handle_trello_exceptions(func):
    """
    A decorator to handle common Trello-related exceptions.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TokenError as e:
            print(f"Token error: {e}")
        except ValueError as e:
            print(f"Value error: {e}")
        except ResourceUnavailable as e:
            print(f"Resource unavailable: {e}")
        except Exception as e: # pylint: disable=broad-except
            print(f"Unexpected error in {func.__qualname__}: {e}")
            traceback.print_exc()
    return wrapper

class TrelloCommands:
    """
    The TrelloCommands class provides functions to interact with the Trello API.
    """

    def __init__(self, config_data: Dict[str, Any]) -> None:
        """
        Initializes the TrelloCommands class with the given configuration.

        Args:
            config_data (Dict[str, Any]):
                The configuration dictionary containing Trello API credentials.
        """

        self.config: Dict[str, Any] = config_data
        self.client: TrelloClient = self.initialize_trello_client()

    def initialize_trello_client(self) -> TrelloClient:
        """
        Initializes and returns a Trello client using credentials from the config.
        
        Returns:
            TrelloClient: An instance of the TrelloClient configured with API credentials.
        """

        config_trello = self.config.get("trello", {})

        api_key = config_trello.get("api_key")
        api_secret = config_trello.get("api_secret")
        oauth_token = config_trello.get("oauth_token")

        # Validate presence of necessary credentials
        if not api_key:
            raise ValueError("Missing Trello API key in the configuration file.")

        # Set environment variables for the Trello client to use
        os.environ["TRELLO_API_KEY"] = api_key
        os.environ["TRELLO_API_SECRET"] = api_secret

        # Initialize Trello client with available credentials
        return TrelloClient(api_key=api_key,
                            api_secret=api_secret,
                            token=oauth_token)

    @handle_trello_exceptions
    def list_boards(self) -> None:
        """
        Lists all Trello boards for the authenticated user.
        """

        boards = self.client.list_boards()
        for board in boards:
            print(f"Board Name: {board.name} - Board ID: {board.id}")

    @handle_trello_exceptions
    def list_lists(self, board_name_or_alias: str) -> None:
        """
        Lists all non-archived lists in a specified Trello board.
        Can use board name or alias from the configuration.

        Args:
            board_name_or_alias (str): The name of the Trello board or an alias.
        """
        # Check if alias exists in config
        alias_info = self.config["trello"].get("alias_ids", {}).get(board_name_or_alias)

        if alias_info:
            board_id = alias_info.get("board_id")
            if not board_id:
                print(f"Error: Alias '{board_name_or_alias}' does not contain a board ID.")
                return
            board = self.client.get_board(board_id)
        else:
            # Fallback to treating it as a board name
            board = next(
                (b for b in self.client.list_boards() if b.name == board_name_or_alias),
                None
            )

        if not board:
            print(f"No board found with the name or alias '{board_name_or_alias}'.")
            return

        # Filter out archived lists (closed == True)
        for list_obj in board.list_lists():
            if not list_obj.closed:
                print(f"List Name: {list_obj.name} - List ID: {list_obj.id}")

    @handle_trello_exceptions
    def list_cards(self, list_name_or_alias: str) -> None:
        """
        Lists all cards in a specified list.
        Can use list name or alias from the configuration.

        Args:
            list_name_or_alias (str): The ID of the list or an alias from the configuration.
        """
        # Check if alias exists in config
        alias_info = self.config["trello"].get("alias_ids", {}).get(list_name_or_alias)

        if alias_info:
            list_id = alias_info.get("list_id")
            if not list_id:
                print(f"Error: Alias '{list_name_or_alias}' does not contain a list ID.")
                return
            list_obj = self.client.get_list(list_id)
        else:
            list_obj = self.client.get_list(list_name_or_alias)

        if not list_obj:
            print(f"No list found with the ID or alias '{list_name_or_alias}'.")
            return

        cards = list_obj.list_cards()
        for card in cards:
            print(f"Card Name: {card.name} - Card ID: {card.id}")

    @handle_trello_exceptions
    def add_board(self, board_name: str) -> None:
        """
        Creates a new board with the specified name.

        Args:
            board_name (str): The name of the board to create.
        """
        new_board = self.client.add_board(board_name)
        print(f"Board '{new_board.name}' created successfully with ID: {new_board.id}")

    @handle_trello_exceptions
    def add_list(self, board_name_or_alias: str, list_name: str) -> None:
        """
        Creates a new list in the specified board.

        Args:
            board_name_or_alias (str): The name of the board or an alias from the configuration.
            list_name (str): The name of the list to create.
        """

        # Check if alias exists in config
        alias_info = self.config["trello"].get("alias_ids", {}).get(board_name_or_alias)

        if alias_info:
            board_id = alias_info.get("board_id")
            if not board_id:
                print(f"Error: Alias '{board_name_or_alias}' does not contain a board ID.")
                return
            board = self.client.get_board(board_id)
        else:
            # Fallback to treating it as a board name
            board = next(
                (b for b in self.client.list_boards() if b.name == board_name_or_alias),
                None
            )

        if not board:
            print(f"No board found with the name or alias '{board_name_or_alias}'.")
            return

        new_list = board.add_list(list_name)
        print(f"List '{new_list.name}' created successfully \
in board '{board.name}' with ID: {new_list.id}")

    @handle_trello_exceptions
    def add_card(self, list_name_or_alias: str, card_name: str, description: str = "") -> None:
        """
        Adds a new card to a specified list.
        Can use list name or alias from the configuration.

        Args:
            list_name_or_alias (str): The name of the list or an alias.
            card_name (str): The name of the card to create.
            description (str, optional): The description for the card.
        """
        # Check if alias exists in config
        alias_info = self.config["trello"].get("alias_ids", {}).get(list_name_or_alias)

        if alias_info:
            list_id = alias_info.get("list_id")
            if not list_id:
                print(f"Error: Alias '{list_name_or_alias}' does not contain a list ID.")
                return
            list_obj = self.client.get_list(list_id)
        else:
            # Fallback to treating it as a list name or ID
            list_obj = self.client.get_list(list_name_or_alias)

        if not list_obj:
            print(f"No list found with the ID or alias '{list_name_or_alias}'.")
            return

        # Add the card to the specified list
        list_obj.add_card(card_name, desc=description)
        print(f"Card '{card_name}' added to list '{list_obj.name}'.")

    @handle_trello_exceptions
    def update_board(self, board_id: str, new_name: str | None = None) -> None:
        """
        Updates the specified board's name.

        Args:
            board_id (str): The ID of the board to update.
            new_name (str): The new name for the board.
        """
        board = self.client.get_board(board_id)
        if new_name:
            board.set_name(new_name)
        print(f"Board '{board_id}' updated successfully.")

    def update_list(self, list_id: str, new_name: str | None = None) -> None:
        """
        Updates the specified list's name.

        Args:
            list_id (str): The ID of the list to update.
            new_name (str): The new name for the list.
        """
        list_obj = self.client.get_list(list_id)
        if new_name:
            list_obj.set_name(new_name)
        print(f"List '{list_id}' updated successfully.")

    @handle_trello_exceptions
    def update_card(self,
                    card_id: str,
                    new_name: str | None = None,
                    new_description: str | None = None) -> None:
        """
        Updates the specified card's name and/or description.

        Args:
            card_id (str): The ID of the card to update.
            new_name (str): The new name for the card (optional).
            new_description (str): The new description for the card (optional).
        """
        card = self.client.get_card(card_id)

        if new_name:
            card.set_name(new_name)
        if new_description:
            card.set_description(new_description)
        print(f"Card '{card_id}' updated successfully.")

    @handle_trello_exceptions
    def delete_board(self, board_id: str) -> None:
        """
        Deletes the specified board.

        Args:
            board_id (str): The ID of the board to delete.
        """
        board = self.client.get_board(board_id)
        board.close()
        print(f"Board '{board_id}' closed successfully.")

    @handle_trello_exceptions
    def delete_list(self, list_id: str) -> None:
        """
        Deletes (closes) the specified list.

        Args:
            list_id (str): The ID of the list to delete.
        """
        list_obj = self.client.get_list(list_id)
        list_obj.close()
        print(f"List '{list}' closed successfully.")

    @handle_trello_exceptions
    def delete_card(self, card_id: str) -> None:
        """
        Deletes the specified card.

        Args:
            card_id (str): The ID of the card to delete.
        """

        card = self.client.get_card(card_id)
        card.delete()
        print(f"Card '{card_id}' deleted successfully.")

    def handle_trello_commands(self, args: argparse.Namespace) -> None:
        """
        Handle Trello commands based on the provided arguments.

        Args:
            args (argparse.Namespace): The parsed command-line arguments.
        """

        if args.boards:
            self.list_boards()
        elif args.lists:
            if args.lists:
                self.list_lists(args.lists)
            else:
                print("Error: Missing argument for listing lists.")
        elif args.cards:
            if args.cards:
                self.list_cards(args.cards)
            else:
                print("Error: Missing argument for listing cards.")
        elif args.add_board:
            if args.add_board:
                self.add_board(args.add_board)
            else:
                print("Error: Missing argument for adding board.")
        elif args.add_list:
            if len(args.add_list) >= 2:
                self.add_list(args.add_list[0], args.add_list[1])
            else:
                print("Error: Missing arguments for adding list. Requires board and list names.")
        elif args.add_card:
            if len(args.add_card) >= 2:
                list_name_or_alias = args.add_card[0]
                card_name = args.add_card[1]
                # Use an empty string if description is not provided
                description = args.add_card[2] if len(args.add_card) > 2 else ""
                self.add_card(list_name_or_alias, card_name, description)
            else:
                print("Error: Missing arguments for adding card. Requires list and card name.")
        elif args.update_board:
            if len(args.update_board) >= 2:
                self.update_board(args.update_board[0], args.update_board[1])
            else:
                print("Error: Missing arguments for updating board. ",
                      "Requires board ID and new name.")
        elif args.update_list:
            if len(args.update_list) >= 2:
                self.update_list(args.update_list[0], args.update_list[1])
            else:
                print("Error: Missing arguments for updating list. Requires list ID and new name.")
        elif args.update_card:
            if len(args.update_card) >= 3:
                self.update_card(args.update_card[0], args.update_card[1], args.update_card[2])
            else:
                print("Error: Missing arguments for updating card. ",
                      "Requires card ID, new name, and description.")
        elif args.delete_board:
            if args.delete_board:
                self.delete_board(args.delete_board)
            else:
                print("Error: Missing argument for deleting board.")
        elif args.delete_list:
            if args.delete_list:
                self.delete_list(args.delete_list)
            else:
                print("Error: Missing argument for deleting list.")
        elif args.delete_card:
            if args.delete_card:
                self.delete_card(args.delete_card)
            else:
                print("Error: Missing argument for deleting card.")
