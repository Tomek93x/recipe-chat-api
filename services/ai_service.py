import httpx
from fastapi import HTTPException

from core.config import settings


async def _call_ollama(prompt: str) -> str:
    payload = {
        "model": settings.ollama_model,
        "prompt": prompt,
        "stream": False,
    }
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            r = await client.post(f"{settings.ollama_url}/api/generate", json=payload)
            r.raise_for_status()
            data = r.json()
        result = (data.get("response") or "").strip()
        if not result:
            raise HTTPException(status_code=502, detail="Ollama zwrocila pusta odpowiedz")
        return result
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Nie mozna polaczyc sie z Ollama. Upewnij sie, ze Ollama dziala.",
        )
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Ollama - timeout")
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Blad Ollama: {exc}")



async def generate_recipe(prompt: str) -> str:
    """Dispatcher: wybiera providera na podstawie ustawien."""
    if settings.ai_provider == "openai":
        return await _call_openai(prompt)
    return await _call_ollama(prompt)
