# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN mkdir -p ${CODE_DIR}/jsbsim
WORKDIR ${CODE_DIR}/jsbsim
RUN git clone https://github.com/JSBSim-Team/jsbsim.git

RUN mkdir -p ${CODE_DIR}/experiments
RUN pip install -e git+https://github.com/lauritowal/guidance-flight-env

RUN mkdir -p ${CODE_DIR}/experiments/checkpoints
RUN mkdir -p ${CODE_DIR}/experiments/images

WORKDIR ${CODE_DIR}/experiments
RUN echo "$PWD"