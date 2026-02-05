#!/bin/bash
set -e

echo "Installing ca-certificates and pandoc..."
sudo apt-get update
sudo apt-get install -y ca-certificates pandoc wget curl

# Update CA certificates
sudo update-ca-certificates

echo "Installing tectonic..."
# Download tectonic binary from GitHub releases
# Note: aarch64 Linux only has musl builds available, not gnu
ARCH=$(uname -m)
if [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
    TECTONIC_ARCH="aarch64-unknown-linux-musl"
else
    TECTONIC_ARCH="x86_64-unknown-linux-gnu"
fi

# Use the continuous release which has the latest builds
TECTONIC_URL="https://github.com/tectonic-typesetting/tectonic/releases/download/continuous/tectonic-0.15.0%2B20251006-${TECTONIC_ARCH}.tar.gz"

echo "Downloading tectonic from: $TECTONIC_URL"
# Use curl with SSL verification disabled (for corporate proxy environments)
curl -fsSL --insecure -o tectonic.tar.gz "$TECTONIC_URL" || wget --no-check-certificate -O tectonic.tar.gz "$TECTONIC_URL"
tar -xzf tectonic.tar.gz
sudo mv tectonic /usr/local/bin/
rm tectonic.tar.gz

echo "Setup complete! pandoc and tectonic are now available."
pandoc --version
tectonic -V
