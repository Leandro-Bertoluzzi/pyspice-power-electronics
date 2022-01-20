# Based on: https://github.com/cyber-g/ubuntu-pyspice-std

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

# Create an environment variable to indicate we are inside a container
ENV IN_CONTAINER Yes

# Copy scripts to run
COPY /scripts .

# Run python, with default with a PySpice example
ENTRYPOINT ["python3"]
CMD ["basic-circuits/voltage-divider.py"]