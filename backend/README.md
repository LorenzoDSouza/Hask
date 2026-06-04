## Running with Docker

The fastest way to run the app together with a PostgreSQL database is via Docker Compose.

### Requirements

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose (included with Docker Desktop)

### Setup

1. Create a `.env` file in the `backend/` folder (it is ignored by Git). Example:

   ```env
   # JWT / auth
   SECRET_KEY=change-me-to-a-long-random-secret
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTE=30

   # Database
   DB_USER=hask
   DB_PASSWORD=hask
   DB_NAME=hask
   DB_PORT=5432
   DB_HOST=localhost
   ```

   > `DB_HOST=localhost` is used when running uvicorn directly on your machine.
   > Docker Compose automatically overrides it to `db` for the app container.

2. Build and start the containers:

   ```bash
   docker compose up --build
   ```

   This starts two services:
   - **db** — PostgreSQL 16, with data persisted in a named volume
   - **app** — the FastAPI API; on startup it runs `alembic upgrade head` and then launches uvicorn

3. Access the app:
   - API: <http://localhost:8000>
   - Interactive docs (Swagger): <http://localhost:8000/docs>
   - PostgreSQL: `localhost:5432`

### Useful commands

```bash
# Run in the background
docker compose up --build -d

# Stop the containers
docker compose down

# Stop and also remove the database volume (wipes all data)
docker compose down -v
```

## Alembic

Database migration tool for SQLAlchemy.

Used to:

- create migration history
- update database schema
- keep database structure versioned

Example commands:

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

---

## Installed packages

- **FastAPI**  
  Main framework used to build the REST API.

- **Uvicorn**  
  ASGI server responsible for running the FastAPI application.

- **SQLAlchemy**  
  ORM used to interact with the database using Python classes instead of raw SQL.

- **bcrypt==4.0.1**  
  Password hashing library used to securely encrypt user passwords.  
  Fixed version (`4.0.1`) is used for compatibility with authentication libraries.

- **python-jose[cryptography]**  
  Used to generate and validate JWT authentication tokens.

- **python-multipart**  
  Required for handling form data and file uploads in FastAPI.

---

## References

\ https://fastapi.tiangolo.com/
\ Curso de FastAPI da Hashtag Programação: https://www.youtube.com/watch?v=BtIy2aD8k_w&list=PLpdAy0tYrnKy3TvpCT-x7kGqMQ5grk1Xq
\ https://marcionizzola.medium.com/implementando-o-uso-de-contratos-na-api-65658c529709
\ https://medium.com/@jeremyalvax/fastapi-backend-architecture-model-controller-service-44e920567699
\ https://medium.com/@jasonirvine76/best-practices-for-fastapi-and-applying-it-in-real-project-dae7bf456aa9
