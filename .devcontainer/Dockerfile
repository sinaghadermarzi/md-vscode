FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install pandoc, fonts, and SVG converter
RUN apt-get update && apt-get install -y --no-install-recommends \
    pandoc \
    fonts-open-sans \
    librsvg2-bin \
    curl \
    build-essential \
    procps \
    file \
    git \
    && rm -rf /var/lib/apt/lists/*

# Switch to vscode user for Homebrew installation (Homebrew refuses to run as root)
USER vscode

# Install Homebrew
RUN NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
ENV PATH="/home/linuxbrew/.linuxbrew/bin:${PATH}"

# Install tectonic via brew
RUN brew install tectonic

# Switch back to root for any additional setup, then return to vscode user
USER root
