FROM python:3.13.9

WORKDIR /opt/app


RUN pip install uv
RUN python -m venv .venv
COPY . .
RUN chmod +x /opt/app/start.sh
RUN uv sync


ENTRYPOINT [ "/opt/app/start.sh" ]

