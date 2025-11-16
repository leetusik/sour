"""Dependency injection functions for FastAPI."""

import httpx


async def get_http_client():
    async with httpx.AsyncClient(verify=False) as client:
        yield client
