import aiohttp
import aiofiles
import asyncio
import os
from typing import List

class AIImageGenerator:
    """Asynchronous AI Image Generator using Artbit API."""

    def __init__(self, timeout: int = 60, output_dir: str = "images"):
        self.url = "https://artbit.ai/api/generateImage"
        self.headers = {
            "User-Agent": "AIImageBot/1.0",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.timeout = timeout
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    async def generate_images(self, prompt: str, amount: int = 1) -> List[str]:
        """Generates AI images asynchronously and returns their URLs."""
        payload = {
            "captionInput": prompt,
            "selectedSamples": str(amount)
        }

        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(self.url, json=payload, timeout=self.timeout) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data.get("imgs", [])

    async def download_images(self, img_urls: List[str]) -> List[str]:
        """Downloads and saves generated images asynchronously."""
        saved_files = []

        async with aiohttp.ClientSession() as session:
            tasks = []
            for i, img_url in enumerate(img_urls):
                filename = os.path.join(self.output_dir, f"image_{i+1}.png")
                tasks.append(self._download_image(session, img_url, filename))
                saved_files.append(filename)

            await asyncio.gather(*tasks)

        return saved_files

    async def _download_image(self, session, url: str, filename: str):
        """Helper function to download and save a single image."""
        async with session.get(url, timeout=self.timeout) as resp:
            resp.raise_for_status()
            async with aiofiles.open(filename, "wb") as file:
                await file.write(await resp.read())

async def main():
    generator = AIImageGenerator()
    prompt = "A futuristic city skyline at night"

    img_urls = await generator.generate_images(prompt, amount=2)

    if img_urls:
        saved_files = await generator.download_images(img_urls)
        return img_urls, saved_files

if __name__ == "__main__":
    asyncio.run(main())