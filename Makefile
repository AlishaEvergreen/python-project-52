install:
	uv sync

migrate:
	uv run python3 manage.py migrate

collectstatic:
	uv run python3 manage.py collectstatic --no-input

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

lint:
	uv run ruff check task_manager

format-app:
	uv run ruff check --fix task_manager