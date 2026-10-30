"""Load a local GGUF model with llama-cpp-python."""

import os
from pathlib import Path

_MODEL = None


def _load_model():
    global _MODEL
    if _MODEL is not None:
        return _MODEL

    model_path = Path(os.getenv("MODEL_PATH", "models/model.gguf"))
    if not model_path.is_file():
        raise RuntimeError(
            f"Model file not found: {model_path}. Add a compatible GGUF file "
            "and set MODEL_PATH if it is stored elsewhere."
        )

    try:
        from llama_cpp import Llama
    except ImportError as exc:
        raise RuntimeError(
            "llama-cpp-python is not installed. Install requirements first."
        ) from exc

    _MODEL = Llama(
        model_path=str(model_path),
        n_ctx=int(os.getenv("MODEL_CONTEXT_LENGTH", "2048")),
        verbose=False,
    )
    return _MODEL


def generate_response(prompt: str) -> str:
    """Generate a response using the configured local GGUF model."""
    model = _load_model()
    result = model.create_chat_completion(
        messages=[
            {
                "role": "system",
                "content": (
                    "You provide general health information for educational use. "
                    "Do not diagnose, prescribe, or recommend personal medication "
                    "doses. Encourage professional care when appropriate."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
        max_tokens=400,
    )
    return result["choices"][0]["message"]["content"].strip()
