FROM mcr.microsoft.com/devcontainers/python:3.14-bookworm

# 1. Replicate 'apt-packages' feature
# Keep the distro Python development packages: Nuitka builds use them even
# though the website build itself runs on the image's Python 3.14.
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
# Install the site build tools into the image's Python 3.14 environment.
RUN python3 -m pip install invoke pipenv

# 4. Replicate 'match-host-time-zone' feature
# Your existing postCreateCommand 'dpkg-reconfigure tzdata' handles the configuration,
# we just ensure the package is present.
RUN apt-get update && apt-get -y install tzdata
