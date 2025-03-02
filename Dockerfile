FROM ubuntu:latest

# Add build arguments for GitHub credentials
ARG GITHUB_USER
ARG GITHUB_PAT

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive
# Set deployment flag for production environment
ENV DEPLOYMENT=True

# Install required packages
RUN apt-get update && apt-get install -y \
    vim \
    systemctl \
    curl \
    libicu-dev \
    python3 \
    python3-pip \
    python3-venv \
    git \
    nginx \
    python3-dev \
    build-essential \
    sudo \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create user and set up directories
RUN useradd -m -s /bin/bash esolathomas && \
    echo "esolathomas ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER esolathomas
WORKDIR /home/esolathomas

# Create Python virtual environment
RUN python3 -m venv /home/esolathomas/stsol
ENV PATH="/home/esolathomas/stsol/bin:$PATH"
ENV VIRTUAL_ENV="/home/esolathomas/stsol"
# Create required directories
RUN mkdir ws out && \
    chmod 755 out

# Clone the repository using credentials
COPY . ws

RUN pip install --upgrade pip && \
    pip install -r ws/requirements.txt
    
# Switch back to root for nginx setup
USER root

# Configure nginx
COPY nginx/sola-thomas-site.conf /etc/nginx/conf.d/default.conf
RUN rm -f /etc/nginx/sites-enabled/default

# Copy scripts
RUN chmod +x /home/esolathomas/ws/scripts/start.sh && \
    chmod +x /home/esolathomas/ws/scripts/shutdown.sh && \
    chmod -R 777 /home/esolathomas/ws

# Add start-nginx script
COPY scripts/start-nginx.sh /home/esolathomas/ws/scripts/start-nginx.sh
RUN chmod +x /home/esolathomas/ws/scripts/start-nginx.sh

USER esolathomas

# Expose ports
EXPOSE 80 8000

# Change CMD to use start.sh
CMD ["/home/esolathomas/ws/scripts/start.sh"]
