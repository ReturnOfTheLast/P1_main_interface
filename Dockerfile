# Base the image on python 3.10
FROM python:3.10

# Install dependencies
RUN pip install flask requests pillow

# Copy all files over
COPY . .

# Start the flask server with the docker flag on startup
CMD python app.py --docker
