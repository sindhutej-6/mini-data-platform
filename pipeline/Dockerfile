FROM python:3.10-slim
WORKDIR /pipeline
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY run_pipeline.py .
COPY OpenFoodFacts.csv .
CMD ["python", "run_pipeline.py"]
