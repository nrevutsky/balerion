FROM ubuntu:latest
MAINTAINER Nazar R

RUN apt-get update -y && \
apt-get install -y python2.7 python-pip wget && \
pip install --upgrade pip &&\
pip install Flask &&\
pip install py2neo==2.0.8 &&\
pip install pandas

WORKDIR /app
COPY . /app

RUN python trustar_balerion/setup.py install --force

ENTRYPOINT [ "python" ]
CMD [ "Balerion/views.py" ]
