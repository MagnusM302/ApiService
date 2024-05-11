# Brug et officielt Python runtime som forældre-image
FROM python:3.10-slim

# Sæt arbejdsdirectory i containeren
WORKDIR /app

# Kopiér filen requirements.txt ind i containeren under "/app/"
COPY requirements.txt .

# Installer eventuelle nødvendige pakker specificeret i requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopiér resten af applikationskoden ind i containeren under "/app/"
COPY . .

# Gør port 5005 tilgængelig uden for containeren
EXPOSE 5005

# Kør app.py når containeren lanceres på port 5005
CMD ["python", "app.py", "--host=0.0.0.0", "--port=5005"]
