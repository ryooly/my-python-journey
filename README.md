# Pokemate (1)

A Pokémon-catching game with a **FastAPI** backend and an interactive **CLI** client.
Trainers register an account, log in, and solve a math quiz — their answers are
averaged into a Pokémon ID, which is fetched from the [PokeAPI](https://pokeapi.co)
and saved to a PostgreSQL database.

---

## Features

- **User accounts** — register, log in, and log out with JWT tokens and bcrypt-hashed passwords.
- **Math quiz gate** — catch a Pokémon by answering 5 problems (addition, subtraction,
  multiplication, division, percentages). The averaged result becomes the Pokémon ID.
- **Catch limit** — each trainer can hold a limited number of Pokémon (default: 3).
- **PokeAPI integration** — Pokémon data is fetched live and persisted locally.
- **Layered architecture** — clean separation between API, controller, service, and repository layers.
- **Custom exception system** — a unified `AppException` hierarchy mapped to proper HTTP status codes.

---

## Tech Stack

| Area          | Technology             |
| ------------- | ---------------------- |
| Language      | Python                 |
| Web framework | FastAPI                |
| Server        | Uvicorn                |
| ORM           | SQLAlchemy             |
| Database      | PostgreSQL 16 (Docker) |
| Validation    | Pydantic               |
| Auth          | PyJWT, bcrypt          |
| HTTP client   | requests               |
| Testing       | pytest                 |

---

## Project Structure

```
pokemate/
├── docker-compose.yml          # PostgreSQL 16 service
├── requirements.txt            # Python dependencies
├── learn.py                    # Scratch file (bcrypt experiment)
└── pokemon_machine/            # Main application
    ├── init_db.py              # One-time table creation script
    ├── next_task.md            # Roadmap notes
    ├── game_feature/           # CLI client
    │   ├── cli.py              # Interactive menu (login/register/catch/logout)
    │   └── math_quiz.py        # Quiz logic + Pokémon ID calculation
    ├── parents/
    │   └── auth/               # FastAPI backend (auth module)
    │       ├── api/            # HTTP endpoints
    │       ├── controller/     # Request handlers
    │       ├── services/       # Business logic
    │       ├── repo/           # Database repositories
    │       ├── models/         # SQLAlchemy models
    │       ├── schemas/        # Pydantic schemas
    │       ├── db/             # Engine + session
    │       ├── exceptions/     # Custom exception hierarchy
    │       ├── handlers/       # FastAPI exception handlers
    │       └── global_dependecy/  # Password & token hashing helpers
    ├── pokemon_hunter/         # PokeAPI fetch + Pokémon persistence
    │   ├── calling.py          # Fetch from PokeAPI
    │   ├── services/           # PokemonService
    │   └── repositories/       # PokemonRepository
    └── test/                   # pytest test suite
```

---

## Getting Started

### Prerequisites

- **Python 3.10+**
- **Docker** & Docker Compose (for PostgreSQL)

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the database

```bash
docker-compose up -d
```

This runs PostgreSQL 16 with the following settings:

| Setting  | Value             |
| -------- | ----------------- |
| User     | `postgres`        |
| Password | `password`        |
| Database | `pokemon_machine` |
| Port     | `5433` → `5432`   |

### 3. Initialize the tables

```bash
cd pokemon_machine
python init_db.py
```

### 4. Start the API server

```bash
# from the pokemon_machine/ folder
uvicorn parents.auth.api.auth_api:app --reload --port 8000
```

### 5. Start the CLI client

Open a **second terminal**:

```bash
# from the pokemon_machine/ folder
python -m game_feature.cli
```

---

## API Reference

Base URL: `http://localhost:8000`

| Method | Endpoint         | Description                              |
| ------ | ---------------- | ---------------------------------------- |
| POST   | `/auth/register` | Create a new trainer account             |
| POST   | `/auth/login`    | Authenticate and receive an access token |
| POST   | `/auth/logout`   | Revoke a trainer's refresh token         |

Interactive docs are available at `http://localhost:8000/docs` once the server is running.

### Example — Register

```json
POST /auth/register
{
  "name": "Ash",
  "age": 12,
  "personality": "brave",
  "password": "pikachu123"
}
```

---

## How Catching Works

1. The trainer selects **Get Pokémon** from the CLI menu.
2. The app checks the catch limit (`pokemon_count` vs `pokemon_limit`, default 3).
3. A 5-question math quiz is presented.
4. All answers are summed and divided by 5, then rounded to produce a **Pokémon ID**.
5. That ID is used to fetch the Pokémon from PokeAPI, which is then stored in the database
   and displayed to the trainer.

---

## Running Tests

```bash
# from the pokemon_machine/ folder
pytest
```

---

## Notes

- The database connection string lives in
  `pokemon_machine/parents/auth/db/session.py`.
- JWT settings (secret key, algorithm, token lifetimes) are configured in
  `pokemon_machine/parents/auth/global_dependecy/token_hashing.py`.
- All application commands (`init_db.py`, `uvicorn`, `python -m game_feature.cli`)
  must be run **from the `pokemon_machine/` folder** so imports resolve correctly.
