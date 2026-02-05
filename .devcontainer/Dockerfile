FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install pandoc, texlive (xetex as PDF engine), fonts, and SVG converter
RUN apt-get update && apt-get install -y --no-install-recommends \
    pandoc \
    texlive-xetex \
    texlive-fonts-recommended \
    fonts-open-sans \
    librsvg2-bin \
    && rm -rf /var/lib/apt/lists/*
