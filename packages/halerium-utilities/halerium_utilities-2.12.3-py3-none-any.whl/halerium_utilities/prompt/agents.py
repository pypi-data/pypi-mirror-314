import httpx
import json
import os
from urllib.parse import urljoin

from halerium_utilities.utils.sse import parse_sse_response, parse_sse_response_async


def _prepare_agent_request(board: dict, card_id: str,
                           continue_answer: bool, path: str):

    tenant = os.getenv('HALERIUM_TENANT_KEY', '')
    workspace = os.getenv('HALERIUM_PROJECT_ID', '')
    runner_id = os.getenv('HALERIUM_ID', '')
    base_url = os.getenv('HALERIUM_BASE_URL', '')
    url = urljoin(base_url, "/api"
                            f"/tenants/{tenant}"
                            f"/projects/{workspace}"
                            f"/runners/{runner_id}"
                            "/prompt/agents")

    headers = {'halerium-runner-token': os.getenv('HALERIUM_TOKEN', '')}

    payload = {
        "id": card_id,
        "board": board,
        "continue_answer": continue_answer,
        "path": path,
    }

    return dict(
        method="POST",
        url=url,
        headers=headers,
        json=payload,
        timeout=600,
    )


async def call_agent_async(board: dict, card_id: str,
                           continue_answer: bool = False,
                           path: str = None,
                           parse_data: bool = False):
    """Call a halerium board asynchronously from a Halerium runner.

    Calls the specified card on a board.

    Parameters
    ----------
    board: dict
        The halerium board where you want to trigger a card.
    card_id: str
        The id of the card that you want to call.
    continue_answer: bool
        If you want to continue the answer (true) or you want to regenerate the card from new.
    path: str
        The path to which stateful functions like Python kernels are assigned.
        If no path is provided than these functions are not available.
    parse_data: bool, optional
        Whether to parse the SSE event data as json strings.
        The default is False.

    Returns
    -------
    async_generator
        The generator of the models answer as SSE events.

    Examples
    --------
    >>> board = {"nodes": [...], "edges": [...]}
    >>> card_id = "[card id]"
    >>> gen = agents.call_agent_async(board, card_id)
    >>> async for event in gen: print(event)
    namespace(event='chunk', data='{"chunk": "Hello", "created": "2023-11-28T16:32:56.724070"}')
    namespace(event='chunk', data='{"chunk": "!", "created": "2023-11-28T16:32:56.724526"}')
    namespace(event='chunk', data='{"chunk": " How", "created": "2023-11-28T16:32:56.724673"}')
    namespace(event='chunk', data='{"chunk": " can", "created": "2023-11-28T16:32:56.724804"}')
    namespace(event='chunk', data='{"chunk": " I", "created": "2023-11-28T16:32:56.724941"}')
    namespace(event='chunk', data='{"chunk": " assist", "created": "2023-11-28T16:32:56.725077"}')
    namespace(event='chunk', data='{"chunk": " you", "created": "2023-11-28T16:32:56.725220"}')
    namespace(event='chunk', data='{"chunk": " today", "created": "2023-11-28T16:32:56.725354"}')
    namespace(event='chunk', data='{"chunk": "?", "created": "2023-11-28T16:32:56.725485"}')
    namespace(event='chunk', data='{"chunk": "", "created": "2023-11-28T16:32:56.725611"}')
    """

    async with httpx.AsyncClient() as httpx_client:
        async with httpx_client.stream(**_prepare_agent_request(board, card_id, continue_answer, path)) as response:
            async for event in parse_sse_response_async(response):
                if parse_data:
                    event.data = json.loads(event.data)
                yield event


def call_agent(board: dict, card_id: str,
               continue_answer: bool = False,
               path: str = None,
               parse_data: bool = False):
    """Call a halerium board from a Halerium runner.

    Calls the specified card on a board.

    Parameters
    ----------
    board: dict
        The halerium board where you want to trigger a card.
    card_id: str
        The id of the card that you want to call.
    continue_answer: bool
        If you want to continue the answer (true) or you want to regenerate the card from new.
    path: str
        The path to which stateful functions like Python kernels are assigned.
        If no path is provided than these functions are not available.
    parse_data: bool, optional
        Whether to parse the SSE event data as json strings.
        The default is False.

    Returns
    -------
    async_generator
        The generator of the models answer as SSE events.

    Examples
    --------
    >>> board = {"nodes": [...], "edges": [...]}
    >>> card_id = "[card id]"
    >>> gen = agents.call_agent(board, card_id)
    >>> for event in gen: print(event)
    namespace(event='chunk', data='{"chunk": "Hello", "created": "2023-11-28T16:32:56.724070"}')
    namespace(event='chunk', data='{"chunk": "!", "created": "2023-11-28T16:32:56.724526"}')
    namespace(event='chunk', data='{"chunk": " How", "created": "2023-11-28T16:32:56.724673"}')
    namespace(event='chunk', data='{"chunk": " can", "created": "2023-11-28T16:32:56.724804"}')
    namespace(event='chunk', data='{"chunk": " I", "created": "2023-11-28T16:32:56.724941"}')
    namespace(event='chunk', data='{"chunk": " assist", "created": "2023-11-28T16:32:56.725077"}')
    namespace(event='chunk', data='{"chunk": " you", "created": "2023-11-28T16:32:56.725220"}')
    namespace(event='chunk', data='{"chunk": " today", "created": "2023-11-28T16:32:56.725354"}')
    namespace(event='chunk', data='{"chunk": "?", "created": "2023-11-28T16:32:56.725485"}')
    namespace(event='chunk', data='{"chunk": "", "created": "2023-11-28T16:32:56.725611"}')
    """

    with httpx.Client() as httpx_client:
        with httpx_client.stream(**_prepare_agent_request(board, card_id, continue_answer, path)) as response:
            for event in parse_sse_response(response):
                if parse_data:
                    event.data = json.loads(event.data)
                yield event
