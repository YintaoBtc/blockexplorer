# Pull base image
FROM python:3.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /scripts

# Install dependencies
RUN python -m pip install \
        pyzmq \
        asyncio \
        request

# Copy project
COPY . /scripts/