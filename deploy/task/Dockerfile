FROM python:3.13

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install poetry

COPY . /app

RUN poetry install
ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]