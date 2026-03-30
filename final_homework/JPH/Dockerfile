FROM python:3.14-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g configurable-http-proxy

RUN pip install --no-cache-dir jupyterhub jupyterlab

CMD ["jupyterhub", "--ip=0.0.0.0", "--port=8000"]