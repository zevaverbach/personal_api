FROM python:3.8
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
COPY . /tmp/personal_api
RUN pip install -e /tmp/personal_api
ENV PERSONAL_API_SQLALCHEMY_DATABASE_URL postgresql://doadmin:q606mxj40xfltziw@zev-api-db-do-user-246213-0.db.ondigitalocean.com:25060/defaultdb
CMD gunicorn -w 4 -k uvicorn.workers.UvicornWorker personal_api.main:app -b 0.0.0.0
