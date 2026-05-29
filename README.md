## Dependencies

### Database

```bash
pip install "psycopg[binary]"
```

- **psycopg[binary]**  
  PostgreSQL driver for Python.  
  Responsible for allowing Python and SQLAlchemy to communicate with the PostgreSQL database.

---

### Environment Variables

```bash
pip install python-dotenv
```

- **python-dotenv**  
  Allows Python to load environment variables from a `.env` file.

Used to keep sensitive information such as:

- database username
- password
- host
- port
- database name

out of the source code for security purposes.

The `.env` file is ignored by Git (`.gitignore`) to avoid exposing credentials in the repository.

Example `.env`:

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5433
DB_NAME=hask
```

---

### Database Migrations

```bash
pip install alembic
```

- **Alembic**  
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

### API & Authentication

```bash
pip install fastapi uvicorn sqlalchemy bcrypt==4.0.1 "python-jose[cryptography]" python-multipart
```

#### Installed packages

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


-------------

## References
\ https://fastapi.tiangolo.com/
\ Curso de FastAPI da Hashtag Programação: https://www.youtube.com/watch?v=BtIy2aD8k_w&list=PLpdAy0tYrnKy3TvpCT-x7kGqMQ5grk1Xq
\ https://marcionizzola.medium.com/implementando-o-uso-de-contratos-na-api-65658c529709
\ https://medium.com/@jeremyalvax/fastapi-backend-architecture-model-controller-service-44e920567699