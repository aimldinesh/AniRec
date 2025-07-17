# ✅ Use a minimal base image with Python installed
FROM python:slim

# ✅ Set environment variables
# Prevent Python from writing .pyc files and enable real-time logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ✅ Set the working directory inside the container
WORKDIR /app

# ✅ Install system dependencies required by LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ✅ Copy all application files into the container
COPY . .

# ✅ Install Python packages in editable mode (supports live updates during development)
RUN pip install --no-cache-dir -e .

# ✅ Train the model before starting the Flask app
# Ensures the latest model is available when the container starts
RUN python pipeline/training_pipeline.py

# ✅ Expose Flask app's port
EXPOSE 5000

# ✅ Define the default command to run when the container starts
CMD ["python", "app.py"]