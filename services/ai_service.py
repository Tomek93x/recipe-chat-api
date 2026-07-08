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


async def _call_openai(prompt: str) -> str:
    if not settings.openai_api_key:
        raise HTTPException(status_code=500, detail="Brak OPENAI_API_KEY w .env")

    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    try:
        resp = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": "Jestes pomocnikiem kulinarnym. Odpowiadaj po polsku.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Blad OpenAI: {exc}")


async def _call_gemini(prompt: str) -> str:
    if not settings.gemini_api_key:
        raise HTTPException(status_code=500, detail="Brak GEMINI_API_KEY w .env")

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{settings.gemini_model}:generateContent"
    )
    payload = {
        "system_instruction": {
            "parts": [{"text": "Jestes pomocnikiem kulinarnym. Odpowiadaj po polsku."}]
        },
        "contents": [{"parts": [{"text": prompt}]}],
    }
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": settings.gemini_api_key,
    }
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            r = await client.post(url, json=payload, headers=headers)
            r.raise_for_status()
            data = r.json()
        candidates = data.get("candidates") or []
        if not candidates:
            raise HTTPException(status_code=502, detail="Gemini zwrocilo pusta odpowiedz")
        parts = candidates[0].get("content", {}).get("parts", [])
        result = "".join(p.get("text", "") for p in parts).strip()
        if not result:
            raise HTTPException(status_code=502, detail="Gemini zwrocilo pusta odpowiedz")
        return result
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502, detail=f"Blad Gemini: {exc.response.status_code} {exc.response.text}"
        )
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Gemini - timeout")
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Blad Gemini: {exc}")


async def generate_recipe(prompt: str) -> str:
    """Dispatcher: wybiera providera na podstawie ustawien."""
    if settings.ai_provider == "openai":
        return await _call_openai(prompt)
    if settings.ai_provider == "gemini":
        return await _call_gemini(prompt)
    return await _call_ollama(prompt)