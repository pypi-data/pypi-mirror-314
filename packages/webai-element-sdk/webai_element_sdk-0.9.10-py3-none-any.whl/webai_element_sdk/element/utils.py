import asyncio
import time

import aiohttp


async def check_server_status_until_success_or_timeout(url: str, timeout: int = 10):
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        error: Exception = None
        while True:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        print("Server is up and returning HTTP 200")
                        await asyncio.sleep(1)
                        return
            except aiohttp.ClientError as e:
                print(e)
                error = e

            if time.time() - start_time > timeout:
                print("Timeout reached without receiving HTTP 200")
                raise error

            await asyncio.sleep(0.5)
