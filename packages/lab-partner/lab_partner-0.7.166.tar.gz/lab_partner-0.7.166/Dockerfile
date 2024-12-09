FROM python:3.10-slim
ARG LAB_VERSION

ENV LAB_VERSION=$LAB_VERSION
ENV LAB_ROOT=/opt/lab
ENV LAB_DIST=${LAB_ROOT}/dist
ENV LAB_BUILD=${LAB_ROOT}/build

RUN apt-get update -y --allow-releaseinfo-change \
  && apt-get install -y \
    git \
    --no-install-recommends

RUN pip install --upgrade pip build \
    && mkdir -p ${LAB_DIST}

COPY . ${LAB_BUILD}
RUN cd ${LAB_BUILD} \
    && python -m build \
    && cp -R ${LAB_BUILD}/dist ${LAB_DIST}/init
