FROM python:3.7.8-alpine

COPY requirements.txt ./
COPY CRM ./

RUN apk update
RUN apk add busybox-extras vim bash expect
RUN pip install -r requirements.txt
RUN cd CRM

CMD ["python", "./manage.py", "runserver", "0.0.0.0:5000"]