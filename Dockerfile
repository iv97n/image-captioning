# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy pyproject.toml and poetry.lock to the working directory
COPY pyproject.toml poetry.lock /app/

# Install dependencies defined in pyproject.toml
RUN poetry install --no-root --no-dev

# Copy the rest of the application code
COPY . /app/

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the Streamlit app
CMD ["poetry", "run", "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
