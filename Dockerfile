FROM python:3.9.0a5-alpine3.10

COPY . /drone_nebula

RUN pip install -r /drone_nebula/requirements.txt

WORKDIR /drone_nebula

CMD ["python", "/drone_nebula/drone_nebula_runner.py"]