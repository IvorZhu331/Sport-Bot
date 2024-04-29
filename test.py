import aiohttp
import asyncio

async def fetch_data():
    url = 'http://ergast.com/api/f1/current'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.text()
                print(data)
            else:
                print("Failed to fetch data:", response.status)

loop = asyncio.get_event_loop()
loop.run_until_complete(fetch_data())
