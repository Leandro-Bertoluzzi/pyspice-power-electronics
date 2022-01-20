FROM ubuntu:focal
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && apt-get upgrade -y

# Install minimal dependencies
RUN apt install -y git python3 python3-pip ngspice libngspice0-dev

# Install PySpice : pip pulls all the python depencies
RUN pip3 install PySpice

# Move to root folder
WORKDIR /root

# Install an additional package for enabling graphics output with python on docker
RUN apt-get install -y python3-tk

# Validate PySpice installation
RUN pyspice-post-installation --check-install

# Copy scripts to run
COPY . .

# Run PySpice example
ENTRYPOINT python3 ac-dc-converters/full-converter.py