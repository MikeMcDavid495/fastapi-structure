# Use an official Python runtime as a base image
FROM python:3.10

# Set environment variables for the database connection
EXPOSE 8000

# Install any necessary dependencies
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Copy the FastAPI application files to the container
COPY . /app

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]