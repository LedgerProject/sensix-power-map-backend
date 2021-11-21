#!/bin/bash

PYENV=${HOME}/.pyenv/bin/pyenv
PYTHON_VERSION=${PYTHON_VERSION:="3.6"}

echo " * Install python version ${PYTHON_VERSION}"

eval "$(${PYENV} init -)"

echo " * Available pyenv versions:"
${PYENV} versions

${PYENV} install --skip-existing "${PYTHON_VERSION}"
${PYENV} local "${PYTHON_VERSION}"
python --version 2>&1 | grep "${PYTHON_VERSION}"

echo " * Upgrade pip"
pip install -U pip

echo " * Install project requirements"
pip install -r requirements.txt

echo " * Migrate database"
python manage.py migrate --noinput --settings=project.settings.tests.codeship