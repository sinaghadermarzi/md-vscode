FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install pandoc, tectonic (PDF engine), fonts, and SVG converter
RUN apt-get update && apt-get install -y --no-install-recommends \
    pandoc \
    fonts-open-sans \
    librsvg2-bin \
    && rm -rf /var/lib/apt/lists/*

# Install tectonic
RUN curl --proto '=https' --tlsv1.2 -fsSL https://drop-sh.fullyjustified.net | sh \
    && mv tectonic /usr/local/bin/
