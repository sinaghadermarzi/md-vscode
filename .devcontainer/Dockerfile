FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install pandoc from official Ubuntu repos (stable version)
RUN apt-get update && apt-get install -y \
    ca-certificates \
    pandoc \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install tectonic - use cargo for a reliable, versioned install
# This avoids volatile GitHub release URLs
RUN apt-get update && apt-get install -y \
    cargo \
    libssl-dev \
    libfontconfig1-dev \
    pkg-config \
    && cargo install tectonic --version 0.15.0 \
    && cp /root/.cargo/bin/tectonic /usr/local/bin/tectonic \
    && apt-get remove -y cargo libssl-dev pkg-config \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* /root/.cargo

# Verify installations
RUN pandoc --version && tectonic -V
