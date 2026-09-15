FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Copy dependency requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy dashboard app
COPY . .

# Expose port
EXPOSE 8501

# Run Streamlit on container launch
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]