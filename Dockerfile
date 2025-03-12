FROM python:3
ADD . /wayf
WORKDIR /wayf
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT ["./gunicorn.sh"]
