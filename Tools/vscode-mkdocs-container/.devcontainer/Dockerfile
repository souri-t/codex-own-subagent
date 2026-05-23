FROM python:3.11-slim

# Install Java (required for PlantUML) and Graphviz
RUN apt-get update && apt-get install -y \
    default-jre \
    graphviz \
    fonts-noto-cjk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install MkDocs and plugins
RUN pip install --no-cache-dir \
    mkdocs \
    mkdocs-material \
    plantuml-markdown \
    mkdocs-static-i18n \
    mkdocs-drawio

WORKDIR /workspace
