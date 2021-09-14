FROM continuumio/miniconda3

RUN mkdir -p /notebooks && \
    mkdir -p /scripts && \
    mkdir -p /test

RUN conda install -c nsls2forge bluesky caproto

# Add epics binary folder to path
ENV PATH="/opt/conda/epics/bin/linux-x86_64:$PATH" 

# Install dev version of ophyd from github repo
WORKDIR /ophyd
RUN git clone https://github.com/bluesky/ophyd.git . && \
    pip install -r requirements.txt && \
    pip install -r requirements-test.txt && \
    pip install -e .

# Install any other python packages via pip
WORKDIR /tmp
COPY requirements.txt .
RUN pip install -r requirements.txt && \
    rm requirements.txt

RUN conda install -c conda-forge jupyterlab -y --quiet

