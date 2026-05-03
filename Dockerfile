# Use lightweight Python image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy files
COPY requirements.txt ./requirements.txt
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose the port Streamlit uses
EXPOSE 8080

# Command to run the app
CMD ["streamlit", "run", "lms_app.py", "--server.port=8080", "--server.address=0.0.0.0"]