"""Simple environment configuration helpers."""

import os


def get_env(key: str, default=None):
    return os.environ.get(key, default)
