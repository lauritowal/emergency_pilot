FROM python:3.7

RUN python3 -m pip install --upgrade pip

RUN git clone https://github.com/JSBSim-Team/jsbsim.git

RUN git clone https://github.com/lauritowal/guidance-flight-env
WORKDIR ${CODE_DIR}/guidance-flight-env
RUN pip3 install -e .

COPY ./experiments ${CODE_DIR}/experiments
RUN mkdir -p ${CODE_DIR}/experiments/checkpoints
RUN mkdir -p ${CODE_DIR}/experiments/images

RUN pip install tensorboard
RUN pip install wandb

WORKDIR ${CODE_DIR}/experiments
CMD ["python3", "sincos_no_wind.py"]