FROM python:3.8
COPY requirements.txt /tmp
RUN pip install -r requirements.txt
COPY . /tmp/personal_api
RUN pip install /tmp/personal_api
CMD gunicorn -w 4 -k uvicorn.workers.UvicornWorker main.app:app
