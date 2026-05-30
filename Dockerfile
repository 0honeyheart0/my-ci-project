FROM python@sha256:a3ab0b966bc4e91546a033e22093cb840908979487a9fc0e6e38295747e49ac0

WORKDIR /app

COPY requirements.txt . requirements.lock ./
RUN pip install --no-cache-dir -r requirements.lock

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
