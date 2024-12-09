FROM python:3.10-slim

ARG LAB_VERSION

ENV LAB_VERSION=$LAB_VERSION
ENV LAB_ROOT=/opt/lab
ENV LAB_DIST=${LAB_ROOT}/dist
ENV LAB_HOME=${LAB_ROOT}/home
ENV LAB_BUILD=${LAB_ROOT}/build
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV PATH ${PATH}:/opt/bin
ENV HOME=${LAB_HOME}
ENV USER ${USER}
ENV DOCKER_VERSION "26.1.2"
ENV DOCKER_COMPOSE_VERSION "2.27.1"
ENV DOCKER_PLUGIN_PATH="/usr/local/lib/docker/cli-plugins"
ENV DOCKER_GID=998
ENV ACT_VERSION "0.2.57"

RUN apt-get update -y --allow-releaseinfo-change \
  && apt-get install -y \
    apt-transport-https \
    openssl \
    locales \
    ca-certificates \
    curl \
    gnupg2 \
    bash-completion \
    vim \
    sudo \
    git \
    gettext-base \
    libc-bin \
    pv \
    unzip \
    jq \
    python3-pip \
    python3-wheel \
    procps \
    dnsutils \
    net-tools \
    iputils-ping \
    openssh-client \
    --no-install-recommends \
  && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
  && locale-gen \
  && mkdir -p /opt/bin

RUN echo "Installing Docker client" \
  && curl -sSL https://download.docker.com/linux/static/stable/$(uname -m)/docker-${DOCKER_VERSION}.tgz > /tmp/docker-latest.tgz \
  && tar -xf /tmp/docker-latest.tgz -C /tmp \
  && cp -R /tmp/docker/* /usr/bin \
  && rm -rf /tmp/docker*

COPY --from=docker/buildx-bin /buildx ${DOCKER_PLUGIN_PATH}/docker-buildx
RUN echo "Installing Docker Compose" \
  && curl -sSL https://github.com/docker/compose/releases/download/v${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m) > ${DOCKER_PLUGIN_PATH}/docker-compose \
  && chmod +x ${DOCKER_PLUGIN_PATH}/docker-compose

RUN echo "Installing act to run github workflows locally" \
  && curl -sSL https://github.com/nektos/act/releases/download/v${ACT_VERSION}/act_$(uname -s)_$(uname -m).tar.gz > /tmp/act.tar.gz \
  && tar -xf /tmp/act.tar.gz -C /tmp \
  && mv /tmp/act /usr/bin/act \
  && rm -rf /tmp/act*

COPY requirements.txt /tmp/cli-requirements.txt
RUN echo "Installing Python dependencies" \
  && pip install --upgrade pip \
  && pip install -r /tmp/cli-requirements.txt

RUN echo "Creating docker group membership" \
    && addgroup docker --gid ${DOCKER_GID} \
    && usermod -aG docker root

COPY bashrc ${HOME}/.bashrc
COPY start-cli.sh /opt/bin/
COPY cli_sudoers /etc/sudoers.d/

CMD ["/opt/bin/start-cli.sh"]