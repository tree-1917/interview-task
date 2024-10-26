# [1] Base Image
FROM python:3.10-slim

# [2] Working Dir
WORKDIR /app

# [3] Move requirements.txt 
COPY requirements.txt .

# [4] Install packages 
RUN pip install --timeout=5000 -r requirements.txt

# [5] Copy project files
COPY . .

# [6] Expose port
EXPOSE 8000

# [7] Run Server 
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
