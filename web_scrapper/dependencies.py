from fastapi import Body
from loguru import logger

from .scraper import extract_urls, fetch_all
from .schema import TextModelRequest

async def get_url_content(body : TextModelRequest = Body(...)) -> str:
    urls = extract_urls(body.prompt)
    if urls:
        try:
            urls_content = await fetch_all(urls)
            return urls_content
        except Exception as e:
            logger.warning(f"Failed to fetcch one or several URLS - ERROR: {e}")
    return ""
