FROM python:3.8

WORKDIR /app

COPY . /app/

RUN apt update
RUN apt install btop -y 
RUN apt install curl -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3", "app.py"]
