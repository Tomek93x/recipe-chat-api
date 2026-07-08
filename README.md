# Recipe Chat API

Aplikacja FastAPI + MongoDB + AI do generowania przepisów z podanych składników.
Użytkownicy logują się, wybierają kategorię (śniadanie / obiad / kolacja) i rozmawiają z AI.
Historia rozmów zapisywana jest per użytkownik w MongoDB i dostępna w panelu historii.

**Live demo:** https://recipe-chat-api.onrender.com
*(darmowy plan Render usypia po 15 min bezczynności — pierwsze wejście po przerwie może potrwać 30-50s)*

## Funkcje

- Rejestracja i logowanie (JWT)
- Chat z AI podzielony na kategorie: śniadanie / obiad / kolacja
- Historia rozmów per użytkownik, z panelem do przeglądania starszych czatów
- Trzy dostępne providery AI: Gemini, OpenAI, Ollama (konfigurowalne przez `.env`)

## Szybki start (lokalnie)

1. Skopiuj `.env.example` do `.env` i uzupełnij wartości
2. Wygeneruj `SECRET_KEY`: `openssl rand -hex 32` (lub `python -c "import secrets; print(secrets.token_hex(32))"`)
3. Uruchom MongoDB: `docker compose up -d mongo`
4. Zainstaluj zależności: `pip install -r requirements.txt`
5. Odpal aplikację: `uvicorn main:app --reload`
6. Otwórz http://localhost:8000

### Wybór providera AI (lokalnie)

W `.env` ustaw `AI_PROVIDER` na jedną z wartości:

- `gemini` — darmowy, szybki, wymaga `GEMINI_API_KEY` (Google AI Studio). Uwaga: dla kont z UE/EOG/Szwajcarii/UK może wymagać podpiętej płatności zgodnie z aktualnymi warunkami Google.
- `openai` — wymaga `OPENAI_API_KEY` i doładowanego konta (brak darmowego tieru)
- `ollama` — całkowicie lokalne i darmowe, ale wymaga zainstalowanej Ollamy (`ollama pull llama3.1` lub mniejszy model jak `llama3.2:3b`) i wolniejsze na CPU bez GPU

## Endpointy API

- `POST /auth/register` – rejestracja
- `POST /auth/login` – logowanie (form data: username, password) → token JWT
- `GET /auth/me` – dane zalogowanego
- `POST /chat/send` – wyślij wiadomość w konwersacji
- `GET /chat/{conversation_id}/messages` – pobierz historię danej konwersacji
- `GET /conversations/` – lista wszystkich konwersacji zalogowanego użytkownika
- `POST /recipes/generate` – jednorazowe generowanie przepisu (bez zapisu do historii)

## Deploy

Aplikacja jest wdrożona na **Render** (Docker, plan Free) i połączona z:
- **MongoDB Atlas** (darmowy klaster M0) jako baza danych
- **Gemini API** jako provider AI na produkcji

Aby wdrożyć własną kopię:
1. Załóż darmowy klaster na [MongoDB Atlas](https://www.mongodb.com/cloud/atlas), dodaj `0.0.0.0/0` do Network Access (wymagane, bo hosting ma dynamiczne IP)
2. Wygeneruj klucz API na [Google AI Studio](https://aistudio.google.com) (Gemini)
3. Na [Render](https://render.com): New → Web Service → połącz repo z GitHub → Render automatycznie wykryje `Dockerfile`
4. Ustaw zmienne środowiskowe z `.env.example` (możesz wkleić cały `.env` naraz przez "Add from .env")
5. Deploy — każdy kolejny `git push origin main` wywoła automatyczny redeploy

## Stack

- FastAPI + Beanie (ODM) + MongoDB
- AI: Gemini (produkcja) / OpenAI / Ollama (lokalnie, konfigurowalne)
- Frontend: czysty HTML/CSS/JS serwowany przez FastAPI
- Docker, wdrożenie na Render