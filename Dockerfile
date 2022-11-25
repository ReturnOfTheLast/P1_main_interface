FROM python:3.10

RUN pip install flask requests pillow

COPY . .

CMD python app.py --docker
