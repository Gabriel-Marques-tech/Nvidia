from graphiti_core.embedder.client import EmbedderClient
from sentence_transformers import SentenceTransformer


class LocalEmbedder(EmbedderClient):
    def __init__(self, model_name: str = "intfloat/multilingual-e5-large"):
        self.model = SentenceTransformer(model_name)

    async def create(self, input_data) -> list[float]:
        if isinstance(input_data, str):
            input_data = [input_data]
        embeddings = self.model.encode(input_data, normalize_embeddings=True)
        return embeddings[0].tolist()