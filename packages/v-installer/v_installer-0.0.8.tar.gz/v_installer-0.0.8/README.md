# Build package

```bash
python3 setup.py sdist bdist_wheel
```

# Publish package to Pypi

```bash
twine upload dist/*
```

# Docker environment

```bash
docker run -it --rm -v $(pwd):/workspace/v-installer python:3.12.7-alpine /bin/sh

apk update
cd /workspace/v-installer
python3 -m pip install setuptools
python3 setup.py sdist bdist_wheel
apk add twine
apk add gcc python3-dev musl-dev linux-headers
TWINE_USERNAME="__token__" TWINE_PASSWORD="pypi-....................................................." twine upload --non-interactive dist/*
```
