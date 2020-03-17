#docker container run -it -p 80:80 --name openface-flask openface-flask:<tag>

FROM algebr/openface

RUN apt-get update && apt-get install -y \
    software-properties-common

RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR '/home/openface-build/deploy'

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

WORKDIR '/home/openface-build/build/bin'
RUN mkdir uploaded

WORKDIR '/home/openface-build/deploy'
ENTRYPOINT ["python3", "app.py"]