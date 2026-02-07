"""
FastMCP Football Server (FastMCP 3.x)
"""

import logging
from typing import Any, Optional

import httpx
from fastmcp import FastMCP

# Logging setup
logging.basicConfig(level=logging.ERROR, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Create server
mcp = FastMCP("Football Server")

FOOTBALL_API_BASE = "https://api.sportsworldcentral.com"


async def make_football_request(url: str) -> dict[str, Any] | None:
    """Make a request to the SportsWorldCentral API with proper error handling."""
    logger.debug(f"Requesting URL: {url}")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.exception(f"Request failed: {e}")
            return None


def format_count(data: dict) -> str:
    return (
        f"\nLeague_Count: {data.get('league_count', 'Unknown')}"
        f"\nTeam_Count: {data.get('team_count', 'Unknown')}"
        f"\nPlayer_Count: {data.get('player_count', 'Unknown')}\n"
    )


@mcp.tool
async def get_counts() -> str:
    """Get counts from SportsWorldCentral"""
    url = f"{FOOTBALL_API_BASE}/v0/counts/"
    data = await make_football_request(url)

    if not data:
        logger.warning("API returned no data.")
        return "Unable to fetch counts."

    return format_count(data)

#Server entrypoint
if __name__ == "__main__":
    mcp.run()  