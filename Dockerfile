FROM python:3.8
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
COPY . /tmp/personal_api
RUN pip install -e /tmp/personal_api
