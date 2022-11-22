FROM python:3.10

RUN pip install flask requests

COPY . .

CMD python app.py --docker
