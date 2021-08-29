FROM continuumio/miniconda3

RUN conda install -c nsls2forge ophyd
RUN conda install -c nsls2forge bluesky caproto

RUN conda install -c conda-forge jupyterlab -y --quiet
RUN mkdir -p /opt/notebooks

# Add epics binary folder to path
ENV PATH="/opt/conda/epics/bin/linux-x86_64:$PATH" 




