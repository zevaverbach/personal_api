FROM python:3.8
COPY . /usr/src/app
RUN cd /usr/src/app && pip install -r requirements.txt
ENV PERSONAL_API_SQLALCHEMY_DATABASE_URL postgresql://doadmin:q606mxj40xfltziw@zev-api-db-do-user-246213-0.db.ondigitalocean.com:25060/defaultdb
ENV PERSONAL_API_USERNAME zev
ENV PERSONAL_API_PASS 14Yearszz
CMD gunicorn -w 4 -k uvicorn.workers.UvicornWorker personal_api.main:app -b 0.0.0.0:80 --preload --access-logfile /var/log/access.log --log-level info --error-logfile /var/log/error.log
