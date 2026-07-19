# Step 1: Use an official lightweight Python runtime as a base image
FROM python:3.10-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of your application code
COPY . .

# Step 6: Expose the port your IRIS API runs on (commonly 8000 or 5000)
EXPOSE 8000

# Step 7: Define the command to run the API (assuming FastAPI/Uvicorn)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]