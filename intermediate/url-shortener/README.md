# url-shortener

A RESTful URL shortening service built with **FastAPI** and **PostgreSQL**. Supports full CRUD operations on short URLs and tracks access statistics per short code.

> **Source:** [roadmap.sh — URL Shortening Service](https://roadmap.sh/projects/url-shortening-service)

---

## Demo

> 🚧 Coming soon

---

## Features

- Generate a unique short code for any long URL
- Resolve a short code back to its original URL
- Update the destination URL behind an existing short code
- Delete a short URL by its short code
- Retrieve access statistics (hit count) for any short code
- Input validation with appropriate HTTP status codes (`400`, `404`, `204`, etc.)
- Minimal frontend for demo purposes

---

## Tech Stack

| Layer      | Technology              |
|------------|-------------------------|
| API        | FastAPI (Python)        |
| Database   | PostgreSQL              |
| ORM        | SQLAlchemy              |
| Runtime    | Uvicorn                 |
| Env Mgmt   | python-dotenv           |
| Frontend   | Vanilla HTML/CSS/JS     |

---

## API Endpoints

| Method   | Endpoint                     | Description                          |
|----------|------------------------------|--------------------------------------|
| `POST`   | `/shorten`                   | Create a new short URL               |
| `GET`    | `/shorten/{shortCode}`       | Retrieve the original URL            |
| `PUT`    | `/shorten/{shortCode}`       | Update the destination URL           |
| `DELETE` | `/shorten/{shortCode}`       | Delete a short URL                   |
| `GET`    | `/shorten/{shortCode}/stats` | Get access count for a short URL     |

---

## Project Structure

```
url-shortener/
├── app/
│   ├── main.py          # FastAPI app entry point, CORS, lifespan
│   ├── database.py      # Engine, session factory, Base
│   ├── init_db.py       # Table creation on startup
│   ├── models.py        # SQLAlchemy ORM model
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── repository.py    # URLRepository — all DB operations
│   ├── service.py       # URLService — business logic
│   └── routers/
│       └── shorten.py   # Route handlers + dependency injection
├── frontend/
│   └── index.html       # Demo UI
├── .env                 # Local env variables (git-ignored)
├── .env.example         # Env variable template
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL running locally

### Clone the repo

```bash
git clone https://github.com/shayansoh/mini-projects.git
cd mini-projects/intermediate/url-shortener
```

### Set up the virtual environment

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configure environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/url_shortener
```

### Create the database

```bash
sudo service postgresql start
sudo -u postgres psql -c "CREATE DATABASE url_shortener;"
```

### Start the API

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.
Interactive docs (Swagger UI) at `http://localhost:8000/docs`.

### Run the frontend

No build step required. Open `frontend/index.html` directly in your browser:

```bash
# from the project root
open frontend/index.html        # macOS
xdg-open frontend/index.html    # Linux/WSL
```

Make sure the API is running before opening the frontend.
