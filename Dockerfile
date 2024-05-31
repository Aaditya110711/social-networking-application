# Use the official Ubuntu image from the Docker Hub
FROM ubuntu:20.04

# Prevent prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory inside the container
WORKDIR /app

# Install Python and other dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    libpq-dev \
    && apt-get clean

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/
# Run Django migrations during the build process
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

# Expose port 8000 to the outside world
EXPOSE 8000

# Start the Django development server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]