# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /usr/src/app

# Install dependencies
COPY requirement.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirement.txt

# Copy the current directory contents into the container at /usr/src/app/
COPY . /usr/src/app/

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "120", "citation_project.wsgi:application"]
