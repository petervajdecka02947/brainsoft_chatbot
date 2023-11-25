FROM python:3.10.12-slim

RUN pip install --no-cache-dir --upgrade pip  && \
    pip install --no-cache-dir setuptools wheel

COPY ./cli /cli

WORKDIR /cli

RUN  pip install --no-cache-dir -r requirements.txt 

ENTRYPOINT ["python"]