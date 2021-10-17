FROM python:3.8-slim-buster

RUN apt update -y && apt upgrade -y

RUN useradd --user-group --system --create-home --no-log-init pythonuser

WORKDIR /auth0

RUN chown -R pythonuser:pythonuser /auth0 \
    && chmod 755 /auth0

ADD requirements.txt /auth0

USER pythonuser

RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python", "app.py", "-h", "0.0.0.0"]