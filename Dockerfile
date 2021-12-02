FROM python:3.8.12-bullseye

COPY . /home/appuser/app/
WORKDIR /home/appuser/app/
RUN pip install -r requirements.txt && \
    python3 setup.py install && \
    addgroup appgroup && \
    adduser appuser --ingroup appgroup --disabled-password --home /home/appuser/ --gecos "App User,RoomNumber,WorkPhone,HomePhone" && \
    chown -R appuser:appgroup /home/appuser/
USER appuser

CMD ["sh", "-c", "python3 manage.py $APP_COMAND"]