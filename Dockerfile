

# Install Python and pip
RUN apt-get update && \
apt-get install -y python3 python3-pip

# Copy requirements and install Python packages
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Set environment variables
ENV POSTGRES_PASSWORD=docker
ENV POSTGRES_DB=world

# Copy SQL init script (optional for your DB schema)
COPY world.sql /docker-entrypoint-initdb.d/