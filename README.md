# fastapi-crud-postgres

A small CRUD REST API for managing products, built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) 0.115 — web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) 2.0 — ORM
- [PostgreSQL](https://www.postgresql.org/) 17 — database
- [Uvicorn](https://www.uvicorn.org/) — ASGI server
- [psycopg2](https://www.psycopg.org/) — PostgreSQL driver
- Python 3.10+

## Project Structure

| File                 | Purpose                                              |
| -------------------- | ---------------------------------------------------- |
| `main.py`            | FastAPI app and route handlers                       |
| `config.py`          | Loads settings from the environment (`.env`)         |
| `database.py`        | SQLAlchemy engine, session, and `get_db` dependency  |
| `models.py`          | `Product` ORM model (table `products`)               |
| `schemas.py`         | `Products` Pydantic request schema                   |
| `compose.yml`        | Docker Compose for PostgreSQL + pgAdmin              |
| `requirements.txt`   | Python dependencies                                  |
| `.env.example`       | Template for the environment variables               |
| `tests/`             | pytest test suite                                    |
| `test_main.http`     | Sample HTTP requests                                 |

## Data Model

The `products` table:

| Column        | Type        | Notes                          |
| ------------- | ----------- | ------------------------------ |
| `id`          | integer     | primary key, auto-generated    |
| `title`       | string      | required                       |
| `description` | string      | required                       |
| `at_sale`     | boolean     | defaults to `false`            |
| `inventory`   | integer     | required, defaults to `0`      |
| `added_at`    | timestamptz | defaults to `now()`            |

## Getting Started

### 1. Configure environment variables

All database and pgAdmin credentials are read from the environment. Copy the
template and adjust the values for your setup:

```bash
cp .env.example .env
```

The `.env` file is gitignored, so your secrets stay out of version control.
Available variables:

| Variable          | Default              | Description                          |
| ----------------- | -------------------- | ------------------------------------ |
| `DB_HOST`         | `localhost`          | PostgreSQL host                      |
| `DB_PORT`         | `5432`               | PostgreSQL port                      |
| `DB_NAME`         | `ecommerce`          | Database name                        |
| `DB_USER`         | `hendisantika`       | Database user                        |
| `DB_PASSWORD`     | —                    | Database password (**required**)     |
| `PGADMIN_EMAIL`   | `admin@localhost.com`| pgAdmin login email (Docker only)    |
| `PGADMIN_PASSWORD`| `admin`              | pgAdmin login password (Docker only) |

### 2. Provide a PostgreSQL database

You can either use an existing local PostgreSQL instance (make sure the database
named in `DB_NAME` exists) or spin one up with Docker Compose, which reads the
same `.env`:

```bash
docker compose up -d        # starts PostgreSQL (5432) and pgAdmin (5050)
```

pgAdmin will be available at http://localhost:5050 with the server pre-configured
via `pgadmin.json` (it authenticates using the credentials from `.env`).

### 3. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Run the app

```bash
uvicorn main:app --reload
```

The API starts on http://127.0.0.1:8000. Tables are created automatically on
startup. Interactive docs are available at http://127.0.0.1:8000/docs.

### 5. Run the tests

```bash
pytest
```

The tests use FastAPI's `TestClient` and require a reachable database configured
via `.env`.

## API Endpoints

| Method   | Path            | Description                    | Body            |
| -------- | --------------- | ----------------------------- | --------------- |
| `GET`    | `/`             | Health check                  | —               |
| `POST`   | `/product`      | Create a product              | `Product` JSON  |
| `GET`    | `/product`      | List all products             | —               |
| `PUT`    | `/update/{id}`  | Update a product by id        | `Product` JSON  |
| `DELETE` | `/delete/{id}`  | Delete a product by id (`204`)| —               |

### Request body

```json
{
  "title": "Widget",
  "description": "A test widget",
  "at_sale": true,
  "inventory": 10
}
```

### Examples

```bash
# Health check
curl http://127.0.0.1:8000/

# Create a product
curl -X POST http://127.0.0.1:8000/product \
  -H 'Content-Type: application/json' \
  -d '{"title":"Widget","description":"A test widget","at_sale":true,"inventory":10}'

# List products
curl http://127.0.0.1:8000/product

# Update product 1
curl -X PUT http://127.0.0.1:8000/update/1 \
  -H 'Content-Type: application/json' \
  -d '{"title":"Widget v2","description":"Updated","at_sale":false,"inventory":25}'

# Delete product 1
curl -X DELETE http://127.0.0.1:8000/delete/1
```

## License

This project is provided as-is for learning purposes.
