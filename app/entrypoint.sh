#!/bin/bash

if [[ -z "${APP_DEBUG}" ]]; then
  UVICORN_FLAGS="--reload"
fi

uvicorn main:app ${UVICORN_FLAGS} --host 0.0.0.0 --port ${PORT}
