import asyncio
import aiohttp
import aiofiles
import concurrent.futures as C_F
from multiprocessing import cpu_count
from bs4 import BeautifulSoup
from math import floor


async def get_response(num_pages, output_file):
    async with aiohttp.ClientSession() as Client, \
    aiofiles.open(output_file, "a", encoding='utf-8') as file:
        for _ in range(num_pages):
            async with Client.get("https://en.wikipedia.org/wiki/Special:Random") as response:
                if response.status != 200:
                    response.raise_for_status()
                page = await response.text()
                soup = BeautifulSoup(page, features="html.parser")
                title = soup.find("h1").text

                await file.write(title +"\n")
        await file.write("\n")

def start_parsing(num_pages, output_file):
    asyncio.run(get_response(num_pages, output_file))


def main():
    NUM_PAGES = 100
    NUM_CORES = cpu_count()
    OUTPUT_FILE = './wiki_titles.txt'

    PAGES_PER_CORE = floor(NUM_PAGES/NUM_CORES)
    PAGES_FOR_FINAL = NUM_PAGES - PAGES_PER_CORE * NUM_CORES

    futures = []

    with C_F.ProcessPoolExecutor(NUM_CORES) as executor:
        for i in range(NUM_CORES):
            new_future = executor.submit(
                start_parsing, 
                num_pages=PAGES_PER_CORE, 
                output_file=OUTPUT_FILE)
            futures.append(new_future)

        futures.append(executor.submit(
                start_parsing, 
                num_pages=PAGES_FOR_FINAL, 
                output_file=OUTPUT_FILE))

    C_F.wait(futures)

if __name__ == "__main__":
    main()




