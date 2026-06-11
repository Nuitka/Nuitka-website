FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

# 1. Replicate 'apt-packages' feature
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    python3-dev \
    python3-pip \
    python-is-python3 \
    python3-lxml \
    bash-completion \
    optipng \
    jpegoptim \
    file \
    patchelf \
    ccache \
    supervisor \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 2. Replicate 'node' feature (Version 20)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 3. Replicate 'bash-command' feature
# Note: Expanded --break to --break-system-packages which is the standard for Ubuntu 24.04 (PEP 668)
RUN python3 -m pip install --break-system-packages invoke pipenv

# 4. Replicate 'match-host-time-zone' feature
# Your existing postCreateCommand 'dpkg-reconfigure tzdata' handles the configuration,
# we just ensure the package is present.
RUN apt-get update && apt-get -y install tzdata
