# pizza-delivery-backend
Implementing the backend of a pizza delivery service is a study of FastApi + Database + Access control/verification, etc.

# Setup
```
poetry init

Dependencies: fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose[cryptography] python-dotenv python-multipart

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