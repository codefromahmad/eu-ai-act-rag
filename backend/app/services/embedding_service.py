class EmbeddingService:
    _model = None

    @classmethod
    def _get_model(cls):
        if cls._model is None:
            from sentence_transformers import SentenceTransformer

            cls._model = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2",
                device="cpu",
            )

        return cls._model

    def embed_text(
        self,
        text: str,
    ) -> list[float]:
        model = self._get_model()

        embedding = model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()