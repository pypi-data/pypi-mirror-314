import json
from typing import Any, Dict, List, Optional, TextIO, Tuple, Union

from halerium_utilities.board import Board
from halerium_utilities.board import schemas
from halerium_utilities.board.connection_rules.node_connectors import NODE_CONNECTORS
from halerium_utilities.logging.exceptions import (
    BoardConnectionError, CardTypeError, PromptChainError)


class BoardNavigator:
    """
    Class to navigate through a Halerium board.
    """

    def __init__(self, board: Union[Dict[str, Any], schemas.Board, Board]):
        """
        Initialize the BoardNavigator with a board.

        Parameters
        ----------
        board : Union[Dict[str, Any], schemas.Board, Board]
            The board to navigate.
        """
        if not isinstance(board, Board):
            board = Board(board)
        self.board = board
        self.cards = {card.id: card for card in self.board.cards}
        self.connections = {connection.id: connection
                            for connection in self.board.connections}
        self.connections_lookup = None
        self._construct_connections_lookup()

    @classmethod
    def from_json(cls, file: Union[str, TextIO]) -> 'Board':
        """
        Create a BoardNavigator instance from a JSON file or file-like object.

        Parameters
        ----------
        file : Union[str, TextIO]
            A file path as a string or a file-like object to read the JSON data from.

        Returns
        -------
        BoardNavigator
            An instance of the BoardNavigator class initialized with the data from the JSON.
        """
        board = Board.from_json(file)
        return cls(board)

    def _construct_connections_lookup(self):
        """
        Construct a lookup for connections.
        """
        connections_lookup = {}
        for card in self.cards.values():
            connections_lookup[card.id] = {}
            for connector in NODE_CONNECTORS[card.type]:
                connections_lookup[card.id][connector.name] = {
                    "source": [], "target": []}

        for connection in self.connections.values():
            source_id = connection.connections.source.id
            source_connector = connection.connections.source.connector
            connections_lookup[source_id][source_connector]["source"].append(connection.id)

            target_id = connection.connections.target.id
            target_connector = connection.connections.target.connector
            connections_lookup[target_id][target_connector]["target"].append(connection.id)

        self.connections_lookup = connections_lookup

    def get_card_type(self, id: str) -> str:
        """
        Get the type of a card.

        Parameters
        ----------
        id : str
            The id of the card.

        Returns
        -------
        str
            The type of the card.
        """
        return self.cards[id].type

    def is_note_card(self, id: str) -> bool:
        """
        Check if a card is a note card.

        Parameters
        ----------
        id : str
            The id of the card.

        Returns
        -------
        bool
            True if the card is a note card, False otherwise.
        """
        return self.get_card_type(id) == "note"

    def is_setup_card(self, id: str) -> bool:
        """
        Check if a card is a setup card.

        Parameters
        ----------
        id : str
            The id of the card.

        Returns
        -------
        bool
            True if the card is a setup card, False otherwise.
        """
        return self.get_card_type(id) == "setup"

    def is_bot_card(self, id: str) -> bool:
        """
        Check if a card is a bot card.

        Parameters
        ----------
        id : str
            The id of the card.

        Returns
        -------
        bool
            True if the card is a bot card, False otherwise.
        """
        return self.get_card_type(id) == "bot"

    def is_vectorstore_card(self, id: str) -> bool:
        """
        Check if a card is a vectorstore card.

        Parameters
        ----------
        id : str
            The id of the card.

        Returns
        -------
        bool
            True if the card is a vectorstore card, False otherwise.
        """
        return self.get_card_type(id) == "vector-store-file"

    def is_frame_card(self, id: str) -> bool:
        """
        Check if a card is a (transparent) frame card

        Parameters
        ----------
        id : str
            The id of the card.

        Returns
        -------
        bool
            True if the card is a frame card, False otherwise.
        """
        return self.get_card_type(id) == "frame"

    def _get_card_bounding_box(self, id):
        card = self.cards[id]
        bounds_x = [card.position.x, card.position.x + card.size.width]
        bounds_y = [card.position.y, card.position.y + card.size.height]
        return [bounds_x, bounds_y]

    @staticmethod
    def _calc_collision(bounds_1, bounds_2):
        # check overlap on x axis
        x_overlap = not (bounds_1[0][1] < bounds_2[0][0] or bounds_1[0][0] > bounds_2[0][1])
        # check overlap on y axis
        y_overlap = not (bounds_1[1][1] < bounds_2[1][0] or bounds_1[1][0] > bounds_2[1][1])
        # if both axes overlap the boxes overlap
        return x_overlap and y_overlap

    def get_frame_ids(self, id: str) -> List[str]:
        """
        Get all ids of cards that are (partially) within the frame card frame.

        Parameters
        ----------
        id : str
            The id of the frame card.

        Returns
        -------
        list
            List of card ids that are within the frame.

        """

        if not self.is_frame_card(id):
            raise CardTypeError(f"id {id} does not belong to a frame.")

        frame_box = self._get_card_bounding_box(id)

        frame_members = []
        for card in self.cards:
            if card == id:
                continue  # skip self
            card_box = self._get_card_bounding_box(card)
            if self._calc_collision(frame_box, card_box):
                frame_members.append(card)

        return frame_members

    def get_containing_frame_ids(self, id: str) -> List[str]:
        """
        Gett all ids of frames that are (partially) containing
        the given card.

        Parameters
        ----------
        id : str
            The id of the card.

        Returns
        -------
        list
            List of frame card ids that are containing the given card.
        """

        card_box = self._get_card_bounding_box(id)

        containing_frames = []
        for card in self.cards:
            if self.is_frame_card(card):
                if card == id:
                    continue  # skip self
                frame_box = self._get_card_bounding_box(card)
                if self._calc_collision(frame_box, card_box):
                    containing_frames.append(card)

        return containing_frames

    def get_prompt_input(self, id: str) -> Optional[str]:
        """
        Get the prompt input of a card.

        Parameters
        ----------
        id : str
            The id of the card.

        Returns
        -------
        Optional[str]
            The prompt input of the card if available.
        """
        prompt_input = getattr(self.cards[id].type_specific, "prompt_input", None)
        return prompt_input

    def get_prompt_output(self, id: str) -> Optional[str]:
        """
        Get the prompt output of a card.

        Parameters
        ----------
        id : str
            The id of the card.

        Returns
        -------
        Optional[str]
            The prompt output of the card if available.
        """
        prompt_output = getattr(self.cards[id].type_specific, "prompt_output", None)
        return prompt_output

    def is_vectorstore_success(self, id: str) -> bool:
        """
        Check if a vectorstore card is successful.

        Parameters
        ----------
        id : str
            The id of the card.

        Returns
        -------
        bool
            True if the vectorstore card's state is `success`

        Raises
        ------
        CardTypeError
            If the card is not a vectorstore card.
        """
        if not self.is_vectorstore_card(id):
            raise CardTypeError(f"Card {id} is not a vectorstore card but of type {self.get_card_type(id)}.")
        success = getattr(self.cards[id].type_specific, "state", None)
        return success == "success"

    def get_vectorstore_file_name(self, id: str) -> str:
        """
        Get the file name of a vectorstore card.

        Parameters
        ----------
        id : str
            The id of the card.

        Returns
        -------
        str
            The file name.

        Raises
        ------
        CardTypeError
            If the card is not a vectorstore card.
        """
        if not self.is_vectorstore_card(id):
            raise CardTypeError(f"Card {id} is not a vectorstore card but of type {self.get_card_type(id)}.")
        file_name = getattr(self.cards[id].type_specific, "vector_store_file", "")
        return file_name.split("/")[-1]

    def get_setup_args(self, id: str) -> Optional[Dict[str, Any]]:
        """
        Get the setup arguments of a card.

        Parameters
        ----------
        id : str
            The id of the card.

        Returns
        -------
        Optional[Dict[str, Any]]
            The setup arguments of the card if the card type has them.
        """
        setup_args = getattr(self.cards[id].type_specific, "setup_args", None)
        return setup_args

    def get_functions_runner_id(self, id: str) -> Optional[str]:
        """
        Get the runner id of the runner assigned to the setup card.

        Parameters
        ----------
        id : str
            The id of the card. Has to be a bot card or setup card.

        Returns
        -------
        Optional[str]
            The id of the runner or None if no runner was found.
        """
        setup_card_id = self.get_setup_card_id(id)
        setup_args = self.get_setup_args(setup_card_id)
        runner_id = setup_args.get("runner_id", None)
        return runner_id

    def _get_bot_predecessor_card_id(self, id: str) -> str:
        """
        Get the id of the bot predecessor card.

        Parameters
        ----------
        id : str
            The id of the card.

        Returns
        -------
        str
            The id of the bot predecessor card.

        Raises
        ------
        BoardConnectionError
            If the card has no connector `prompt_input` or no connection to `prompt_input`.
        """
        try:
            conn_id = self.connections_lookup[id]["prompt-input"]["target"][0]
            source_card_id = self.connections[conn_id].connections.source.id
        except KeyError:
            raise BoardConnectionError("Card {id} has no connector `prompt-input`.")
        except IndexError:
            raise BoardConnectionError("Card {id} has no connection to `prompt-input`.")

        return source_card_id

    def get_bot_predecessor_card_id(self, id: str) -> Optional[str]:
        """
        Get the id of the bot predecessor card.

        Parameters
        ----------
        id : str
            The id of the card.

        Returns
        -------
        Optional[str]
            The id of the bot predecessor card, or None if there is no bot predecessor card.
        """
        try:
            return self._get_bot_predecessor_card_id(id)
        except BoardConnectionError:
            return None

    def get_bot_successor_card_ids(self, id: str) -> List[str]:
        """
        Get the ids of the bot successor cards.

        Parameters
        ----------
        id : str
            The id of the card.

        Returns
        -------
        List[str]
            The ids of the bot successor card.
        """
        try:
            conn_ids = self.connections_lookup[id]["prompt-output"]["source"]
            target_card_ids = [
                self.connections[conn_id].connections.target.id
                for conn_id in conn_ids]
            return target_card_ids
        except KeyError:
            raise BoardConnectionError("Card {id} has no connector `prompt-output`.")

    def get_setup_card_id(self, id: str) -> str:
        """
        Get the id of the setup card.

        Parameters
        ----------
        id : str
            The id of the card.

        Returns
        -------
        str
            The id of the setup card.

        Raises
        ------
        PromptChainError
            If the prompt chain could not be traced to a setup card.
        """
        cid = id
        security_loop = 0
        while not self.is_setup_card(cid):
            security_loop += 1
            cid = self.get_bot_predecessor_card_id(cid)
            if cid is None or security_loop > 100:
                raise PromptChainError("Prompt Chain could not be traced to setup card.")

        return cid

    def get_bot_type(self, id: str) -> str:
        """
        Get the type of the bot.

        Parameters
        ----------
        id : str
            The id of the card.

        Returns
        -------
        str
            The type of the bot.
        """
        setup_card_id = self.get_setup_card_id(id)
        return self.cards[setup_card_id].type_specific.bot_type

    def get_note_title(self, id: str) -> str:
        """
        Get the title of a note card.

        Parameters
        ----------
        id : str
            The id of the card.

        Returns
        -------
        str
            The title of the note card.

        Raises
        ------
        CardTypeError
            If the card is not a note card.
        """
        if not self.is_note_card(id):
            raise CardTypeError(f"Card {id} is not a note card but of type {self.get_card_type(id)}.")
        return self.cards[id].type_specific.title

    def get_note_message(self, id: str) -> str:
        """
        Get the message of a note card.

        Parameters
        ----------
        id : str
            The id of the card.

        Returns
        -------
        str
            The message of the note card.

        Raises
        ------
        CardTypeError
            If the card is not a note card.
        """
        if not self.is_note_card(id):
            raise CardTypeError(f"Card {id} is not a note card but of type {self.get_card_type(id)}.")
        return self.cards[id].type_specific.message

    def get_attachments(self, id: str) -> Optional[Dict]:
        """
        Get the attachments of a card.

        Parameters
        ----------
        id : str
            The id of the card.

        Returns
        -------
        Optional[Dict]
            The attachments of the card if the card type has attachments.
        """
        attachments = getattr(self.cards[id].type_specific, "attachments", None)
        return attachments

    def get_context_from_card(self, id: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Get the context from a card.

        Parameters
        ----------
        id : str
            The id of the card.

        Returns
        -------
        Tuple[Optional[str], Optional[str]]
            The title and message of the card, or None for both if the card is not a note or prompt card.
        """
        if self.is_note_card(id):
            title = self.get_note_title(id)
            message = self.get_note_message(id)
        elif self.is_bot_card(id):
            title = None
            message = self.get_prompt_output(id)
        elif self.is_frame_card(id):
            partial_board = self.board.get_partial_board(self.get_frame_ids(id))
            self._drop_attachments(partial_board)
            title = None
            message = json.dumps(partial_board.to_dict())
        else:
            title, message = None, None

        return title, message

    @staticmethod
    def _drop_attachments(board):
        for card in board.cards:
            if hasattr(card.type_specific, "attachments"):
                card.type_specific.attachments = {}

    def get_all_context_card_ids(self, id: str) -> List[str]:
        """
        Get all context card ids.
        If a context card is connected twice, it is returned only once.

        Parameters
        ----------
        id : str
            The id of the card.

        Returns
        -------
        List[str]
            The ids of all context cards.

        Raises
        ------
        ConnectionError
            If the card type has no context input connector.
        """
        try:
            connection_ids = self.connections_lookup[id]["context-input"]["target"]
        except KeyError:
            raise ConnectionError(f"Card {id} of type {self.get_card_type(id)} has no context-input.")

        context_ids = []
        for conn_id in connection_ids:
            context_ids.append(
                self.connections[conn_id].connections.source.id
            )

        return list(set(context_ids))

    def get_content_dependencies(self, id: str) -> List[str]:
        """
        Get all ids of cards (and other nodes) on which the given card or node's
        content depends.

        For example, for a bot card this means all of its context cards as well
        as its predecessor card. For a frame this means all cards contained in it.

        Returns
        -------
        List[str]
            The ids of the dependency cards.
        """

        if self.is_note_card(id):
            return []
        elif self.is_bot_card(id):
            contexts = self.get_all_context_card_ids(id)
            parent = self.get_bot_predecessor_card_id(id)
            parents = [parent] if parent else []
            return parents + contexts
        elif self.is_setup_card(id):
            return self.get_all_context_card_ids(id)
        elif self.is_vectorstore_card(id):
            return []
        elif self.is_frame_card(id):
            return self.get_frame_ids(id)
        else:
            raise NotImplementedError(f"Card type {self.get_card_type(id)} unknown.")

    def get_execution_order(self, id_list: List[str],
                            recursion_error: bool = False,
                            keep_only_executable: bool = True
                            ) -> List[str]:
        """
        Linearize a card tree to get an execution chain
        that follows the order of dependencies.

        Recursions are broken at the first loop unless
        `recursion_error` is set to True.

        Parameters
        ----------
        id_list : List[str]
            The list of card and node ids to linearize
        recursion_error : bool, optional
            Whether recursions are to load to an error or not.
            The default is False.
        keep_only_executable : bool, optional
            Whether to only keep ids of actually executable
            cards in the result.
            The default is True.

        Returns
        -------
        List[str]
            The list of ids to be executed in order.

        """

        dependencies = {}
        for id in id_list:
            dependencies[id] = self.get_content_dependencies(id)

        linear_order = []
        recursion_protection = set()

        def visit(id):
            # check if id was already processed
            if id in linear_order:
                return

            # check if id is currently being processed
            if id in recursion_protection:
                if recursion_error:
                    raise PromptChainError("Circular dependency detected.")
                return
            # add id to currently being processed set
            recursion_protection.add(id)

            deps = dependencies[id]
            # visit all dependencies first
            for d in deps:
                visit(d)

            # check that id was not added in mean time
            if id in linear_order:
                raise PromptChainError("Linearization failed.")
            # add id to linear_order
            linear_order.append(id)

            # remove id from currently being processed set
            recursion_protection.remove(id)

            return

        for id in dependencies:
            visit(id)

        if keep_only_executable:
            linear_order = [
                id for id in linear_order if self.is_bot_card(id)
            ]

        return linear_order
