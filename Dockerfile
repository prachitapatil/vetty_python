FROM python:3.9-slim-buster
# Set the working directory inside the container
WORKDIR /app
# Copy the requirements.txt file to the container
COPY requirements.txt .
# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the application code to the container
COPY . .
# Expose the desired port for the Flask application
EXPOSE 5000
# Run the Flask application
CMD ["flask", "run", "--host", "0.0.0.0"]