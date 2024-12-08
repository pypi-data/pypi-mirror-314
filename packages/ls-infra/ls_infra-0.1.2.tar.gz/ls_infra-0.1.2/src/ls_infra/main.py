# src/ls_infra/main.py
"""Main module for ls-infra package."""
import uvicorn
from ls_infra.api import app
from ls_infra.cli import cli


def run_api(host: str = "0.0.0.0", port: int = 8000):
    """Run the FastAPI application"""
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    cli()
