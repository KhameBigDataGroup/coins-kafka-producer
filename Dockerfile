FROM ubuntu:16.04
MAINTAINER Alireza Tofighi Mohammadi <alirtofighim@gmail.com>
RUN echo "version 1.0.0"
# skip any interactive post-install configuration steps
ENV DEBIAN_FRONTEND noninteractive

RUN sed -i 's|http://us.|http://ir.|g' /etc/apt/sources.list
RUN sed -i 's|http://archive|http://ir.archive|g' /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y ssh python3 python3-dev python3-setuptools python3-pip ipython
RUN apt-get install -y curl vim nano iputils-ping binutils
RUN apt-get install -y libpq-dev libproj-dev gdal-bin
RUN apt-get install -y locales tzdata
RUN apt-get install -y rsyslog cron

RUN echo "Asia/Tehran" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

ADD ./requirements.txt /opt/producer/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade -r /opt/producer/requirements.txt

ADD . /opt/producer

WORKDIR /opt/producer

ENV HTTP_PROXY ''
ENV HTTPS_PROXY ''
ENV TZ=Asia/Tehran
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN chmod +x entrypoint.py
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

ENTRYPOINT ["python3", "entrypoint.py"]