# pizza-delivery-backend
Implementing the backend of a pizza delivery service is a study of FastApi + Database + Access control/verification, etc.

# Setup
```
poetry init

Dependencies: fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose[cryptography] python-dotenv python-multipart sqlalchemy_utils alembic 

Dev dependencies: black isort pytest ruff

poetry install

sudo apt update

sudo apt install make
```

# Makefile set up

```
fmt:
	poetry run black .
	poetry run isort .

lint:
	poetry run ruff check .
```

# DB (sqlalchemy) | DB migration (alembic)
alembic init alembic
|alembic.ini: sqlalchemy.url = sqlite:///database/banco.db <-> |models.py: create_engine("sqlite:///../database/banco.db", echo=True, future=True)
alembic.env.py -> from app import Base + target_metadata = Base.metadata
run poetry alembic revision --autogenerate -m "initial migration"
ruc poetry alembic upgrade head
