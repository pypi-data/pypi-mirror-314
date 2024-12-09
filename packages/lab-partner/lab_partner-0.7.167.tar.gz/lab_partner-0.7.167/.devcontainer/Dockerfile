FROM python:3.10-slim

RUN echo "Add Docker GPG key" \
    && apt-get update \
    && apt-get install -y ca-certificates curl \
    && install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc \
    && chmod a+r /etc/apt/keyrings/docker.asc \
    && echo "Add the Docker repository to Apt sources" \
    && echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y docker-ce-cli docker-buildx-plugin docker-compose-plugin

# install python dependencies 
# RUN pip install tomli==2.0.1 tomli-w==1.0.0
# RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
#     --mount=type=bind,source=.devcontainer/generate-dependency-toml.py,target=generate-dependency-toml.py \
#     ./generate-dependency-toml.py \
#     && pip install /tmp/deps/[test]
