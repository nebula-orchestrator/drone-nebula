FROM python:3.8.1-alpine3.10

COPY . /drone_nebula

RUN pip install -r /drone_nebula/requirements.txt

WORKDIR /drone_nebula

CMD ["python", "/drone_nebula/drone_nebula_runner.py"]