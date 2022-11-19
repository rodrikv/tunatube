FROM python:3.9-slim

# init
ADD . /code
WORKDIR /code

# setup
RUN apt-get update
RUN apt-get install -y ffmpeg
RUN pip3 install -r requirements.txt
CMD [ "python3", "/code/main.py" ]
