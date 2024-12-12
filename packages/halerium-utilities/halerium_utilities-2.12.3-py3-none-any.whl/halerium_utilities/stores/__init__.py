from halerium_utilities.stores.api import add_chunks_to_vectorstore, add_chunks_to_vectorstore_async
from halerium_utilities.stores.chunker import Chunker


def batch_iter(generator, batch_size):
    batch = []
    for item in generator:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch.clear()

    if len(batch) > 0:
        yield batch


def add_to_vectorstore(vectorstore_id: str, chunker: Chunker):

    for chunks in batch_iter(chunker.chunk(), 2):
        add_chunks_to_vectorstore(vectorstore_id, chunks)

