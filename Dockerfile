FROM python:3.9

WORKDIR /app
COPY requirements/ requirements/

RUN apt-get update && apt-get install gettext -y
RUN pip install --upgrade pip
RUN pip install -r ./requirements/local.txt
RUN pip freeze

COPY . /app/

EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]