#!/bin/bash

uv run alembic upgrade head

uv run fastapi run src/app.py