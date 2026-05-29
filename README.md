## Dependencise
\n psycopg[binary] -> driver to link python with postgresql
\n python-dotenv -> this package allow python to read variables from the .venv file
\n will be important to add the steps to add the variables for the db in the .env file that is not in the repositorie (it is in the gitignore) for safety purposes
\n pip install alembic -> for db migrations
\n pip3 install fastapi uvicorn sqlalchemy "passlib[bcrypt]" "python-jose[cryptography]" python-dotenv python-multipart
## References
\ https://fastapi.tiangolo.com/
\ Curso de FastAPI da Hashtag Programação: https://www.youtube.com/watch?v=BtIy2aD8k_w&list=PLpdAy0tYrnKy3TvpCT-x7kGqMQ5grk1Xq
\ https://marcionizzola.medium.com/implementando-o-uso-de-contratos-na-api-65658c529709
\ https://medium.com/@jeremyalvax/fastapi-backend-architecture-model-controller-service-44e920567699