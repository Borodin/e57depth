FROM python:3.9.2-slim-buster

#RUN apt install libxerces-c-dev
ADD requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --ignore-installed
ADD . .

ENTRYPOINT ["python3", "main.py"]