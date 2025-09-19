fmt:
	poetry run black .
	poetry run isort .

lint:
	poetry run ruff check .

run:
	poetry run uvicorn main:app --reload

