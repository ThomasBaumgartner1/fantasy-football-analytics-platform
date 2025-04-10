FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy the entire project into the container
COPY . .
CMD ["python", "src/data_ingestion/fetch_fpl_data.py"]
