FROM python:3.12.4

WORKDIR /root/

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY app .

CMD source deploy.sh

EXPOSE 8000