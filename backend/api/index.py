"""Vercel Python serverless entrypoint.

Exposes the Flask WSGI application as `app`, which Vercel's @vercel/python
runtime detects and serves. All /api/* routes are handled here.
"""
import os
import sys

# Make the backend package importable from this nested entrypoint.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app  # noqa: E402,F401
