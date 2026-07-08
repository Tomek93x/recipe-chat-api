import httpx
from fastapi import HTTPException

from core.config import settings


async def generate_recipe_response(prompt: str) -> str:
    payload = {
        "model": settings.ollama_model,
        "prompt": prompt,
        "stream": False
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{settings.ollama_url}/api/generate",
                json=payload
            )
            response.raise_for_status()
            data = response.json()

        result = data.get("response", "").strip()

        if not result:
            raise HTTPException(
                status_code=502,
                detail="Ollama returned an empty response."
            )

        return result

    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Ollama. Make sure Ollama is installed and running."
        )

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Ollama HTTP error: {exc.response.status_code} - {exc.response.text}"
        )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Ollama request timed out."
        )

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Request to Ollama failed: {str(exc)}"
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected Ollama service error: {str(exc)}"
        )