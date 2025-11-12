FROM browseruse/browseruse:latest

ENV UV_CACHE_DIR=/root/.cache/uv
USER root
WORKDIR /opt/app
ENV HOME=/opt/app


COPY . .
COPY --chmod=+x start.sh /opt/app/start.sh

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked,id=apt-$TARGETARCH$TARGETVARIANT \
    uv venv .venv \
    && uv sync


ENTRYPOINT [ "/opt/app/start.sh" ]

