from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self, model_name="normal"):
        # This uses the working PyTorch engine we already downloaded
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_text(self, chunks):
        # The library specifically looks for this name: 'embed_text'
        # We convert the result to a list so the database can save it
        return self.model.encode(chunks).tolist()

class BaseEmbedder:
    pass