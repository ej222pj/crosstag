FROM ubuntu:latest
MAINTAINER Eric Jennerstrand "ej222pj@student.lnu.se", Kristoffer Svensson "ks222rt@student.lnu.se"
COPY . /cloudtag
WORKDIR /cloudtag
RUN apt-get update -y && apt-get install -y \
  python3-pip \
  python3-dev \
  build-essential \
  unixodbc \
  unixodbc-dev \
  freetds-dev \
  freetds-bin \
  tdsodbc \
  && pip3 install -r requirements.txt
RUN yes | cp -f freeodbcconfig/freetds.conf /etc/freetds/
RUN yes | cp -f freeodbcconfig/odbc.ini /etc/
RUN yes | cp -f freeodbcconfig/odbcinst.ini /etc/
ENTRYPOINT ["python3"]
CMD ["crosstag_server.py"]
