# Use the official Ubuntu as the base image
FROM ubuntu:latest

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1

# Update package lists and install necessary dependencies
RUN apt update -y && apt upgrade -y && \
    apt install -y python3-pip
RUN apt install -y wget unzip

# Install TensorFlow using pip
RUN pip3 install protobuf==3.20.*
RUN pip3 install tensorflow==2.12.1
RUN pip3 install nsfw-detector mitmproxy

RUN wget https://github.com/GantMan/nsfw_model/releases/download/1.1.0/nsfw_mobilenet_v2_140_224.zip && unzip nsfw_mobilenet_v2_140_224.zip

# Clean up the package cache to reduce the image size
# RUN apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

# Start a shell when the container runs
CMD ["/bin/bash"]

