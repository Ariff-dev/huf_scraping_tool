# Usamos una imagen de Python ligera (basada en Debian/Ubuntu)
FROM python:3.10-slim-bullseye

# Prevenir que Python escriba archivos .pyc en el disco del contenedor
ENV PYTHONDONTWRITEBYTECODE 1
# Forzar a que la salida estándar se envíe directo a los logs (útil en Docker)
ENV PYTHONUNBUFFERED 1

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Instalamos gunicorn (servidor web de producción) y el resto de librerías de tu proyecto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Playwright necesita dependencias a nivel del sistema operativo para poder ejecutar Chromium en Ubuntu
# El flag --with-deps se encarga de instalarlas usando apt-get automáticamente
RUN playwright install chromium --with-deps

# Copiamos el código fuente de tu API
COPY . .

# Exponemos el puerto
EXPOSE 5000

# Usamos Gunicorn como servidor WSGI (Reemplaza a tu servidor de prueba de Flask)
# Le asignamos 2 trabajadores y 4 hilos por cada uno para manejar múltiples llamadas a la API a la vez
CMD ["gunicorn", "-w", "2", "--threads", "4", "-b", "0.0.0.0:5000", "main:app"]
