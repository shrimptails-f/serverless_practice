# syntax=docker/dockerfile:1
FROM python:3.9-bookworm AS base

# 環境変数とタイムゾーンの設定
ENV TZ=Asia/Tokyo
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8

# 基本パッケージのインストール
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    apt-get update && \
    apt-get install -y \
    locales \
    zip \
    unzip \
    vim \
    git \
    keychain \
    curl && \
    localedef -i ja_JP -c -f UTF-8 -A /usr/share/locale/locale.alias ja_JP.UTF-8

# AWS CLI インストール
RUN --mount=type=cache,target=/tmp/aws \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/aws/awscliv2.zip" && \
    unzip -o /tmp/aws/awscliv2.zip -d /tmp/aws && \
    /tmp/aws/aws/install

# Python tools インストール
FROM base AS python-tools
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir \
    black \
    flake8 \
    mypy \
    pytest \
    pytest-cov \
    pylint \
    autopep8 \
    isort

# Task Runner インストール
FROM base AS task-runner
RUN --mount=type=cache,target=/tmp/task \
    curl -sL "https://github.com/go-task/task/releases/download/v3.9.0/task_linux_amd64.deb" -o /tmp/task/task.deb && \
    dpkg -i /tmp/task/task.deb

# 最終ステージ
FROM base AS final
# Node.js をインストール
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# Serverless Framework をインストール
RUN --mount=type=cache,target=/root/.npm \
    npm install -g serverless@3

# Python toolsをコピー
COPY --from=python-tools /usr/local/bin /usr/local/bin
COPY --from=python-tools /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages


# Task Runnerをコピー
COPY --from=task-runner /usr/local/bin/task /usr/local/bin/task

# PATHの設定
ENV PATH="/usr/local/bin:$PATH"

# bashrcのコピー
COPY .devcontainer/infra/python/.bashrc /root/.bashrc

# SSH keychain設定
RUN eval `keychain --eval --agents ssh id_rsa`

ENV APP_ROOT /data
WORKDIR $APP_ROOT
