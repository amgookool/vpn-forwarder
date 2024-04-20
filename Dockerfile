FROM python:3.12-slim-bullseye

ENV TZ=America/La_Paz

# Set the working directory
WORKDIR /app
COPY ./driver.py /app/driver.py
COPY ./requirementsLock.txt /app/requirements.txt
COPY ./main.py /app/main.py

RUN apt update && apt install -y wget unzip
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install -y ./google-chrome-stable_current_amd64.deb
RUN rm google-chrome-stable_current_amd64.deb

RUN apt clean

RUN python -m pip install --upgrade pip

RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["python", "main.py"]