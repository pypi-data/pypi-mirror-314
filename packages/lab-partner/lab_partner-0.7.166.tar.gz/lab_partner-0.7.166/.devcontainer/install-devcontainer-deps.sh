#!/bin/sh

apt update && apt install -y \
    curl \
    procps \
    git \
    --no-install-recommends
rm -rf /var/lib/apt/lists/*

