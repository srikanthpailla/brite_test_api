FROM python:3.10.13-slim

WORKDIR  /brite

RUN useradd -m python

COPY . /brite

RUN pip install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:."

ENTRYPOINT [ "uvicorn", "main:app", "--port=8000", "--host=0.0.0.0" ]

USER python