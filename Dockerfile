FROM python:3.10

# Set the working directory inside the Docker image
WORKDIR /wikipedia

# Copy your entire project into the Docker image
COPY . .

# Install the project dependencies
RUN pip install -r requirements.txt --no-cache

# Adjust the working directory to where your Python module's main entry point is located
WORKDIR /wikipedia/src

# Specify the command to run your application
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]