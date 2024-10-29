FROM python:3.12.4

WORKDIR /root/app/

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY app .

CMD sh deploy.sh

EXPOSE 8000