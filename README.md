# Recipe Chat API

Aplikacja FastAPI + MongoDB + AI do generowania przepisów z podanych składników.
Użytkownicy logują się, wybierają kategorię (śniadanie / obiad / kolacja) i rozmawiają z AI.
Historia rozmów zapisywana jest per użytkownik w MongoDB.

## Szybki start (lokalnie)

1. Skopiuj `.env.example` do `.env` i uzupełnij wartości
2. Wygeneruj `SECRET_KEY`: `openssl rand -hex 32`
3. `docker compose up -d`
4. (Pierwszy raz) ściągnij model: `docker compose exec ollama ollama pull llama3.1`
5. Otwórz http://localhost:8000

## Endpointy API

- `POST /auth/register` – rejestracja
- `POST /auth/login` – logowanie (form data: username, password) → token JWT
- `GET /auth/me` – dane zalogowanego
- `POST /chat/send` – wyślij wiadomość w konwersacji
- `GET /chat/{conversation_id}/messages` – pobierz historię
- `GET /conversations/` – lista twoich konwersacji
- `POST /recipes/generate` – jednorazowe generowanie przepisu

## Deploy

Aplikacja jest gotowa do hostingu. Wystarczy:
- Wrzucić repo na Render / Railway / Fly.io / DigitalOcean App Platform
- Ustawić zmienne środowiskowe z `.env.example` (przede wszystkim `SECRET_KEY` i `OPENAI_API_KEY` jeśli nie chcesz Ollamy)
- Udostępnić MongoDB (np. MongoDB Atlas – podaj connection string w `MONGO_URL`)

## Stack
- FastAPI + Beanie (ODM) + MongoDB
- AI: Ollama (lokalnie) / OpenAI (produkcja)
- Frontend: czysty HTML/CSS/JS serwowany przez FastAPI
- Docker + docker-compose
