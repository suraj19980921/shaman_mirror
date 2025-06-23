FROM ubuntu:22.04

RUN apt update && apt install -y python3 python3-pip

WORKDIR /app1

COPY . .

RUN pip3 install -r requirements.txt

CMD ["sh", "-c", "python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000"]


