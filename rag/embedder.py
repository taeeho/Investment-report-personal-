from sentence_transformers import SentenceTransformer
from utils.config import get_embedding_model

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(get_embedding_model())
    return _model


def embed_text(texts):
    model = _get_model()
    if isinstance(texts, str):
        return model.encode([texts])[0].tolist()
    return model.encode(texts).tolist()
