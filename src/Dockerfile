FROM python:3.11.6-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

CMD ["python","-m", "main"]