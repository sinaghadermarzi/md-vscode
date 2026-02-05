FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install pandoc, tectonic (PDF engine), fonts, and SVG converter
RUN apt-get update && apt-get install -y --no-install-recommends \
    pandoc \
    fonts-open-sans \
    librsvg2-bin \
    cargo \
    libssl-dev \
    libfontconfig1-dev \
    && rm -rf /var/lib/apt/lists/*

# Install tectonic via cargo (works on ARM)
RUN cargo install tectonic \
    && mv /root/.cargo/bin/tectonic /usr/local/bin/
