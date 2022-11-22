FROM python:3.10

RUN pip install flask

COPY . .

CMD python app.py --docker
