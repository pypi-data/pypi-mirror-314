import os
from typing import List, Union, Optional, Dict

import httpx

from halerium_utilities.stores.chunker import Document


REQUEST_PARAMETERS = {
    "base_url": None,
    "headers": None,
    "timeout": None
}


def update_request_parameters(base_url=None, headers=None, timeout=None):
    """Update global request parameters."""
    if base_url:
        REQUEST_PARAMETERS["base_url"] = base_url
    if headers:
        REQUEST_PARAMETERS["headers"] = headers
    if timeout:
        REQUEST_PARAMETERS["timeout"] = timeout


def reset_request_parameters():
    """Reset the global request parameters using environment variables."""
    tenant = os.getenv('HALERIUM_TENANT_KEY')
    workspace = os.getenv('HALERIUM_PROJECT_ID')
    runnerId = os.getenv('HALERIUM_ID')
    runnerToken = os.getenv('HALERIUM_TOKEN')
    baseUrl = os.getenv('HALERIUM_BASE_URL')

    update_request_parameters(
        base_url=f"{baseUrl}/api/tenants/{tenant}/projects/{workspace}/runners/{runnerId}/information-store/",
        headers={"halerium-runner-token": runnerToken},
        timeout=120
    )


reset_request_parameters()


class InformationStoreException(Exception):
    """Custom exception for Information Store errors."""
    def __init__(self, msg):
        super().__init__(msg)


def get_workspace_information_stores():
    """Retrieve all information stores in the workspace."""
    url = REQUEST_PARAMETERS["base_url"] + "stores/"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    with httpx.Client() as client:
        response = client.get(url, headers=headers, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("could not set vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


async def get_workspace_information_stores_async():
    """Asynchronously retrieve all information stores in the workspace."""
    url = REQUEST_PARAMETERS["base_url"] + "stores/"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("could not set vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


def get_information_store_info(store_id):
    """Retrieve information about a specific information store."""
    url = REQUEST_PARAMETERS["base_url"] + f"stores/{store_id}/"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    with httpx.Client() as client:
        response = client.get(url, headers=headers, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("could not set vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


async def get_information_store_info_async(store_id):
    """Asynchronously retrieve information about a specific information store."""
    url = REQUEST_PARAMETERS["base_url"] + f"stores/{store_id}/"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("could not set vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


def add_information_store(name):
    """Add a new information store."""
    url = REQUEST_PARAMETERS["base_url"] + "stores/"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    payload = {"name": name}

    with httpx.Client() as client:
        response = client.post(url, headers=headers, json=payload, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("could not set vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


async def add_information_store_async(name):
    """Asynchronously add a new information store."""
    url = REQUEST_PARAMETERS["base_url"] + "stores/"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    payload = {"name": name}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("could not set vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


def rename_information_store(store_id, new_name):
    """Rename an existing information store."""
    url = REQUEST_PARAMETERS["base_url"] + f"stores/{store_id}/"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    payload = {"name": new_name}

    with httpx.Client() as client:
        response = client.put(url, headers=headers, json=payload, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("could not set vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


async def rename_information_store_async(store_id, new_name):
    """Asynchronously rename an existing information store."""
    url = REQUEST_PARAMETERS["base_url"] + f"stores/{store_id}/"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    payload = {"name": new_name}

    async with httpx.AsyncClient() as client:
        response = await client.put(url, headers=headers, json=payload, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("could not set vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


def delete_information_store(store_id):
    """Delete an information store."""
    url = REQUEST_PARAMETERS["base_url"] + f"stores/{store_id}"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    with httpx.Client() as client:
        response = client.delete(url, headers=headers, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("could not set vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


async def delete_information_store_async(store_id):
    """Asynchronously delete an information store."""
    url = REQUEST_PARAMETERS["base_url"] + f"stores/{store_id}"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=headers, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("could not set vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


def add_memory_to_store(store_id, memory: str):
    """Add memory to a specific information store."""
    url = REQUEST_PARAMETERS["base_url"] + f"stores/{store_id}/memories"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    payload = {"memory": memory}

    with httpx.Client() as client:
        response = client.post(url, headers=headers, json=payload, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("could not set vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


async def add_memory_to_store_async(store_id, memory: str):
    """Asynchronously add memory to a specific information store."""
    url = REQUEST_PARAMETERS["base_url"] + f"stores/{store_id}/memories"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    payload = {"memory": memory}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("could not set vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


def add_file_to_vectorstore(vectorstore_id, filepath: str,
                            chunker_args: Optional[Dict[str, Union[str, bool, List[str]]]] = None,
                            metadata: Optional[Dict[str, str]] = None):
    """Add a file to a specific vector store."""
    url = REQUEST_PARAMETERS["base_url"] + f"vectorstore/{vectorstore_id}/files"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    if chunker_args is None:
        chunker_args = dict()

    if metadata is None:
        metadata = dict()

    payload = {
        "filepath": filepath,
        "chunker_args": chunker_args,
        "metadata": metadata
    }

    with httpx.Client() as client:
        response = client.post(url, headers=headers, json=payload, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("could not set vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


async def add_file_to_vectorstore_async(vectorstore_id, filepath: str,
                                        chunker_args: Optional[Dict[str, Union[str, bool, List[str]]]] = None,
                                        metadata: Optional[Dict[str, str]] = None):
    """Asynchronously add a file to a specific vector store."""
    url = REQUEST_PARAMETERS["base_url"] + f"vectorstore/{vectorstore_id}/files"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    if chunker_args is None:
        chunker_args = dict()

    if metadata is None:
        metadata = dict()

    payload = {
        "filepath": filepath,
        "chunker_args": chunker_args,
        "metadata": metadata
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("could not set vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


def add_chunks_to_vectorstore(vectorstore_id, chunks: List[Union[Document, dict]]):
    """Add chunks to a specific vector store."""
    chunks = [Document.validate(c) for c in chunks]

    url = REQUEST_PARAMETERS["base_url"] + f"vectorstore/{vectorstore_id}/chunks/"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    payload = {"chunks": [chunk.dict() for chunk in chunks]}

    with httpx.Client() as client:
        response = client.post(url, headers=headers, json=payload, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("could not add chunks to vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


async def add_chunks_to_vectorstore_async(vectorstore_id, chunks: List[Union[Document, dict]]):
    """Asynchronously add chunks to a specific vector store."""
    chunks = [Document.validate(c) for c in chunks]

    url = REQUEST_PARAMETERS["base_url"] + f"vectorstore/{vectorstore_id}/chunks/"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    payload = {"chunks": [chunk.dict() for chunk in chunks]}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("could not set vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


def query_vectorstore(vectorstore_id, query, max_results=5, post_filter=None):
    """Query a specific vector store."""
    url = REQUEST_PARAMETERS["base_url"] + "vector-store/"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    data = {
        "query": query,
        "max_results": max_results,
        "post_filter": post_filter,
        "threshold": .7,
        "document_id": vectorstore_id,
        "tenant": os.getenv('HALERIUM_TENANT_KEY'),
        "workspace": os.getenv('HALERIUM_PROJECT_ID'),
    }

    with httpx.Client() as client:
        response = client.get(url, params=data, headers=headers, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("could not set vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


async def query_vectorstore_async(vectorstore_id, query, max_results=5, post_filter=None):
    """Asynchronously query a specific vector store."""
    url = REQUEST_PARAMETERS["base_url"] + "vector-store/"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    data = {
        "query": query,
        "max_results": max_results,
        "post_filter": post_filter,
        "threshold": .7,
        "document_id": vectorstore_id,
        "tenant": os.getenv('HALERIUM_TENANT_KEY'),
        "workspace": os.getenv('HALERIUM_PROJECT_ID'),
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=data, headers=headers, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("could not set vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


def get_file_as_text(filepath: str):
    """Retrieve a file as text from the information store."""
    url = REQUEST_PARAMETERS["base_url"] + "files"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    payload = {"filepath": filepath}

    with httpx.Client() as client:
        response = client.get(url, headers=headers, params=payload, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("could not set vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


async def get_file_as_text_async(filepath: str):
    """Asynchronously retrieve a file as text from the information store."""
    url = REQUEST_PARAMETERS["base_url"] + "files"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    payload = {"filepath": filepath}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=payload, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("could not set vectorstore (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


def get_chunks(vectorstore_id: str, start=0, size=1000):
    """Retrieve chunks from a specific vector store."""
    url = REQUEST_PARAMETERS["base_url"] + f"vectorstore/{vectorstore_id}"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    payload = {"start": start, "size": size, "full_chunk_content": True}

    with httpx.Client() as client:
        response = client.get(url, headers=headers, params=payload, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("Error (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


async def get_chunks_async(vectorstore_id: str, start=0, size=1000, full_chunk_content=False):
    """Asynchronously retrieve chunks from a specific vector store."""
    url = REQUEST_PARAMETERS["base_url"] + f"vectorstore/{vectorstore_id}"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    payload = {"start": start, "size": size, "full_chunk_content": full_chunk_content}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=payload, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("Error (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


def get_chunk(vectorstore_id: str, chunk_id: str):
    """Retrieve a specific chunk from a vector store."""
    url = REQUEST_PARAMETERS["base_url"] + f"vectorstore/{vectorstore_id}/chunks/{chunk_id}"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    with httpx.Client() as client:
        response = client.get(url, headers=headers, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("Error (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


async def get_chunk_async(vectorstore_id: str, chunk_id: str):
    """Asynchronously retrieve a specific chunk from a vector store."""
    url = REQUEST_PARAMETERS["base_url"] + f"vectorstore/{vectorstore_id}/chunks/{chunk_id}"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("Error (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


def edit_chunk(vectorstore_id: str, chunk_id: str, document: Union[Document, dict]):
    """Edit a specific chunk in a vector store."""
    document = Document.validate(document)

    url = REQUEST_PARAMETERS["base_url"] + f"vectorstore/{vectorstore_id}/chunks/{chunk_id}"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    with httpx.Client() as client:
        response = client.put(url, headers=headers, json=document.dict(), timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("Error (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


async def edit_chunk_async(vectorstore_id: str, chunk_id: str, document: Union[Document, dict]):
    """Asynchronously edit a specific chunk in a vector store."""
    document = Document.validate(document)

    url = REQUEST_PARAMETERS["base_url"] + f"vectorstore/{vectorstore_id}/chunks/{chunk_id}"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    async with httpx.AsyncClient() as client:
        response = await client.put(url, headers=headers, json=document.dict(), timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("Error (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


def delete_chunks(vectorstore_id: str, chunk_ids: list[str]):
    """Delete specific chunks from a vector store."""
    url = REQUEST_PARAMETERS["base_url"] + f"vectorstore/{vectorstore_id}/chunks/"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    payload = chunk_ids

    with httpx.Client() as client:
        response = client.request("DELETE", url, headers=headers, json=payload, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("Error (%d)...\n%s" % (response.status_code, response.text))

    return response.json()


async def delete_chunks_async(vectorstore_id: str, chunk_ids: list[str]):
    """Asynchronously delete specific chunks from a vector store."""
    url = REQUEST_PARAMETERS["base_url"] + f"vectorstore/{vectorstore_id}/chunks/"
    headers = REQUEST_PARAMETERS["headers"]
    timeout = REQUEST_PARAMETERS["timeout"]

    payload = chunk_ids

    async with httpx.AsyncClient() as client:
        response = await client.request("DELETE", url, headers=headers, json=payload, timeout=timeout)

    if response.status_code != 200:
        raise InformationStoreException("Error (%d)...\n%s" % (response.status_code, response.text))

    return response.json()
