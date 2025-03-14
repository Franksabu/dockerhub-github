FROM python:3.10

# Désactiver la mise en mémoire tampon pour une sortie immédiate
ENV PYTHONUNBUFFERED 1

# Créer un répertoire de travail
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc musl-dev

# Upgrade pip
RUN pip install --upgrade pip

# Copier les fichiers de dépendances
COPY ./requirements.txt .
# Installer les dépendances
RUN pip install -r requirements.txt

# Copier le reste de l'application
COPY ./gestion_budget /app

# Copy the entrypoint script and make it executable
COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh

# Entry command
ENTRYPOINT ["sh", "/entrypoint.sh"]

