# Python 3.11
FROM python:3.11-slim

# Radni direktorijum
WORKDIR /app

# Instalacija sistemskih paketa
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Kopiranje requirements fajla
COPY requirements.txt .

# Instalacija Python biblioteka
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Kopiranje celog projekta
COPY . .

# Kreiranje foldera ako ne postoje
RUN mkdir -p output temp_audio

# Pokretanje aplikacije
CMD ["python3.11", "-m", "app.main"]