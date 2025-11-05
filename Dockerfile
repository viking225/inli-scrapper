FROM python:3.13.9

WORKDIR /opt/app


RUN pip install uv
RUN python -m venv .venv
COPY . .
RUN uv sync


CMD ["uv", "run", "fastapi", "run", "src/main.py", "--no-reload", "--port", "8000"]


