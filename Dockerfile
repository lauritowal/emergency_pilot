FROM python:3.7

ENV CODE_DIR /root/code

RUN python3 -m pip install --upgrade pip

RUN git clone https://github.com/lauritowal/guidance-flight-env
WORKDIR ${CODE_DIR}/guidance-flight-env
RUN pip3 install -e .

RUN mkdir -p ${CODE_DIR}/jsbsim
WORKDIR ${CODE_DIR}/jsbsim
RUN git clone https://github.com/JSBSim-Team/jsbsim.git

COPY ./experiments ${CODE_DIR}/experiments
RUN mkdir -p ${CODE_DIR}/experiments/checkpoints
RUN mkdir -p ${CODE_DIR}/experiments/images

WORKDIR ${CODE_DIR}/experiments
CMD ["python3", "sincos_no_wind.py"]