# Dockerfile for invoice_microservices
FROM my-python-base

# Kopier kun requirements.txt først for at udnytte Docker cache
COPY requirements.txt .
RUN C:\Python310\python.exe -m pip install --no-cache-dir -r requirements.txt

# Kopier hele applikationskoden
COPY . .

# Definer hvilken port applikationen kører på
EXPOSE 5003

# Definer startkommandoen for applikationen
CMD ["C:\\Python310\\python.exe", "run.py", "--host=0.0.0.0", "--port=5003"]
