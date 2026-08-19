from app.config import settings


class EmbeddingService:
    _model = None

    @classmethod
    def _get_model(cls):
        if cls._model is not None:
            return cls._model

        from sentence_transformers import SentenceTransformer

        if settings.embedding_backend == "onnx":
            cls._model = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2",
                backend="onnx",
                model_kwargs={
                    "provider": "CPUExecutionProvider",
                    "file_name": "onnx/model.onnx",
                },
            )
        else:
            cls._model = SentenceTransformer(
                "sentence-transformers/all-MiniLM-L6-v2",
                backend="torch",
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