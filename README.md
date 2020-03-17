This repository is a dockerized version of tadas-openface served on a flask app. 

Given images of faces via post request, this app returns the eye gaze (both position and angle) within the images.

To run for dev environment:

docker-compose up --build 

or 

docker container run -it -p 80:80 mgelisgen/openface-flask:<tag>