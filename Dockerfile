FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install pdm && pdm config python.use_venv false && pdm install

COPY . .

CMD ["pdm", "run", "python", "dashboard.py"]
