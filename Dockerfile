# set base image (host OS)
FROM python:3.9

# set the working directory in the container
WORKDIR /till

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . .

ENV FLASK_APP=till.app

EXPOSE 8000

# command to run on container start
CMD [ "python", "-m", "gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "stock.wsgi:app" ]