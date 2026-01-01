FROM python:3.9-slim

WORKDIR /app

COPY api/ .

RUN pip install --no-cache-dir flask

EXPOSE 5000

CMD ["python", "app.py"]

# # ❌ Mauvaise pratique : image Python obsolète avec CVE connues
# FROM python:3.6

# # ❌ Mauvaise pratique : exécution en root (par défaut)
# WORKDIR /app

# # ❌ Mauvaise pratique : tout copier (y compris secrets, .env, .git)
# COPY . .

# # ❌ Mauvaise pratique : pas de versions figées + dépendances vulnérables
# RUN pip install flask==0.12 \
#     && pip install requests==2.19.1

# # ❌ Mauvaise pratique : variables sensibles en clair
# ENV SECRET_KEY=hardcoded-secret-key
# ENV DEBUG=true

# # ❌ Mauvaise pratique : permissions trop larges
# RUN chmod -R 777 /app

# # ❌ Mauvaise pratique : port exposé sans justification
# EXPOSE 5000

# # ❌ Mauvaise pratique : commande shell non sécurisée
# CMD python app.py
