FROM mgelisgen/openface

RUN apt-get update && apt-get install -y \
    software-properties-common

RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR '/usr/local/deploy'

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

WORKDIR '/usr/local/bin'
RUN mkdir uploaded

WORKDIR '/usr/local/deploy'
ENTRYPOINT ["python3", "app.py"]