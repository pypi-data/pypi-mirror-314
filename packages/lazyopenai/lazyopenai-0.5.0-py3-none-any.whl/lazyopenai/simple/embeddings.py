from openai.types import CreateEmbeddingResponse

from ..client import get_openai_client
from ..settings import get_settings


def create_embeddings(texts: str | list[str]) -> CreateEmbeddingResponse:
    if isinstance(texts, str):
        texts = [texts]

    client = get_openai_client()
    settings = get_settings()

    response = client.embeddings.create(input=texts, model=settings.openai_embedding_model)
    return response
