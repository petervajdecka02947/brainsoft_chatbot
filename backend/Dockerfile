FROM python:3.10.12-slim

RUN apt-get update -y && \
    pip install --upgrade pip

COPY ./backend /backend

WORKDIR /backend

# Set PYTHONPATH to include the /backend directory for pytest
ENV PYTHONPATH /backend

RUN pip install --no-cache-dir -r requirements.txt


ENTRYPOINT ["sh", "entry.sh"]