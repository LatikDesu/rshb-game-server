FROM python:3.11-slim

RUN python3 -m venv /opt/venv/

CMD ["mkdir", "app/server/"]

WORKDIR /app/server/
COPY ./server/ .

RUN /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install -r /app/server/requirements.txt && \
    chmod +x /app/server/scripts/entrypoint.sh && \
    chmod +x /app/server/scripts/createsuperuser.sh && \
    chmod +x /app/server/scripts/migrations.sh && \
    chmod +x /app/server/scripts/collectstatic.sh && \
    chmod +x /app/server/scripts/loaddata.sh && \
    bash /app/server/scripts/collectstatic.sh

CMD ["/app/server/scripts/entrypoint.sh"]