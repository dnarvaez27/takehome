FROM python:3.11.5-slim

# Install poetry
ENV POETRY_VERSION=1.5.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="$PATH:/root/.local/bin"

RUN pip install pipx
RUN pipx install "poetry==$POETRY_VERSION"
RUN pipx ensurepath

RUN mkdir /app
WORKDIR /app

# Install dependencies
COPY pyproject.toml poetry.lock .pylintrc ./
RUN poetry install --no-dev --no-root --no-interaction --no-ansi

# Copy application files
COPY ./src ./src
COPY ./test_data ./test_data
COPY main.py ./

CMD [ "poetry", "run", "python", "main.py" ]
