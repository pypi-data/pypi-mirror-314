FROM enclarify/debian-dind-rootless:11.8-slim-0.9.3
USER root

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y software-properties-common \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
        gnupg2 \
        curl \
        linux-headers-$(dpkg --print-architecture) \
    && add-apt-repository contrib \
    && distribution=$(. /etc/os-release;echo $ID$VERSION_ID | sed -e 's/\.//g') \
    && curl -sSL https://developer.download.nvidia.com/compute/cuda/repos/${distribution}/$(uname -m)/cuda-keyring_1.1-1_all.deb > /tmp/cuda-keyring_1.1-1_all.deb \
    && dpkg -i /tmp/cuda-keyring_1.1-1_all.deb \
    && curl -sSL https://nvidia.github.io/libnvidia-container/gpgkey \
    | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
    && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
    | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
    | tee /etc/apt/sources.list.d/nvidia-container-toolkit.list \
    && apt-get update \
    && apt-get install -y cuda-drivers nvidia-container-toolkit nvidia-container-runtime \
    && sed -i 's|^#no-cgroups.*|no-cgroups = true|' /etc/nvidia-container-runtime/config.toml

USER rootless

# Add the container runtime config to daemon.json
RUN nvidia-ctk runtime configure --runtime=docker --config=${XDG_CONFIG_HOME}/docker/daemon.json