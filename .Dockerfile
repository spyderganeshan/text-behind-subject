# Use official Python image
FROM python:3.9

# Set working directory inside the container
WORKDIR /app

# Copy project files to container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir torch torchvision fastapi uvicorn pillow numpy opencv-python-headless streamlit requests

# Expose FastAPI (8000) and Streamlit (8501) ports
EXPOSE 8000 8501

# Start both FastAPI and Streamlit using a process manager
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 8501 --server.address 0.0.0.0"]
