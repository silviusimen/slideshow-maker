FROM ubuntu:22.04@sha256:77906da86b60585ce12215807090eb327e7386c8fafb5402369e421f44eff17e

ENV DEBIAN_FRONTEND noninteractive

RUN set -e; apt-get -y update; apt-get dist-upgrade -y

RUN set -e; apt-get install -y melt python3 python3-pip 

RUN set -e; apt-get install -y cmt python3-mlt python3-pandas less mc exif ffmpeg 

RUN python3 -m pip install python-dateutil exif geopy ffmpeg-python 
RUN python3 -m pip install dataprep==0.4.0

RUN apt-get install -y git bash-completion python3-cairo python3-pil
RUN python3 -m pip install overpy geotiler urllib3 requests


#RUN set -e; apt-get -yq autoremove; apt-get autoclean

