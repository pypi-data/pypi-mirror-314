FROM python:3.10
WORKDIR /opt/program

ARG TASK_NAME
ARG TASK_MODULE

# prevent python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# make sure that python doesn't use its buffer, which can cause problems by hiding error messages
ENV PYTHONDONTWRITEBYTECODE 1
# add /opt/program to PATH
ENV PATH="/opt/program:${PATH}"

ENV POETRY_VERSION='1.8.3'

ENV TASK_NAME=${TASK_NAME}
ENV TASK_MODULE=${TASK_MODULE}


COPY build /opt/program
COPY src /opt/program/src

RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false
ADD pyproject.toml /opt/program/pyproject.toml
ADD poetry.lock /opt/program/poetry.lock
ADD README.md /opt/program/README.md

RUN export PATH="$HOME/.poetry/bin:$PATH"

RUN poetry install --no-interaction --no-ansi

CMD ["python", "task.py"]