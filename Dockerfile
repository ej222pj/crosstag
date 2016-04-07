FROM ubuntu:latest
MAINTAINER Eric Jennerstrand "ej222pj@student.lnu.se"
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /cloudtag
WORKDIR /cloudtag
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["crosstag_server.py"]
