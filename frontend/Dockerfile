FROM python:3.10.12-slim

RUN pip install --no-cache-dir --upgrade pip  && \
    pip install --no-cache-dir setuptools wheel

COPY ./frontend /frontend
COPY ./.streamlit /.streamlit

RUN chmod +x /frontend/entry.sh

RUN  pip install --no-cache-dir -r /frontend/requirements.txt 

ENTRYPOINT ["./frontend/entry.sh"]