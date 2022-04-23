FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY main_web_service.py main_web_service.py
COPY solver.py solver.py

CMD [ "python3", "main_web_service.py"]

