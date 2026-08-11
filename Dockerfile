FROM python@sha256:a3ab0b966bc4e91546a033e22093cb840908979487a9fc0e6e38295747e49ac0

WORKDIR /app

RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 appuser 

COPY requirements.txt . requirements.lock ./
RUN pip install --no-cache-dir -r requirements.lock

COPY .. .

USER appuser

EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:5000/health || exit 1

CMD ["python", "app.py"]
