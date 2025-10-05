import asyncio
import re

import aiohttp
from bs4 import BeautifulSoup
from loguru import logger

def extract_urls(text: str) -> list[str]:
    url_pattern = r"https?://[^\s\"'<>]+"
    urls = re.findall(url_pattern,text)
    return urls

def parse_inner_text(html_string : str) -> str:
    soup = BeautifulSoup(html_string, "lxml")
    if content := soup.find("div", {"id":"mw-content-text"}):
        return content.get_text(strip=True)
    logger.warning("could not parse the html contet")
    return ""

async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
            if response.status != 200:
                logger.error(f"HTTP {response.status} for {url}")
                return ""
            
            html_string = await response.text()
            logger.info(f"Fetched {len(html_string)} chars from {url}")
            
            return parse_inner_text(html_string=html_string)
            
    except aiohttp.ClientError as e:
        logger.error(f"Network error fetching {url}: {e}")
        return ""
    except Exception as e:
        logger.error(f"Error processing {url}: {e}")
        return ""

async def fetch_all(urls :list[str]) -> str:
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            *[fetch(session,url) for url in urls], return_exceptions=True
        )
    success_result = [result for result in results if isinstance(result,str)]
    if len(results) != len(success_result):
        logger.warning("some urls couldnt be fetched")
    return "".join(success_result)