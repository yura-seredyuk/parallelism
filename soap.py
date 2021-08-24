import asyncio
import aiohttp
import aiofiles
import concurrent.futures as C_F
from multiprocessing import cpu_count
from bs4 import BeautifulSoup
from math import floor


async def get_response():
    async with aiohttp.ClientSession() as Client:
    # aiofiles.open(output_file, "a", encoding='utf-8') as file:
        # for _ in range(num_pages):
        async with Client.get("https://www.ukr.net/") as response:
            if response.status != 200:
                response.raise_for_status()
            page = await response.text()
            soup = BeautifulSoup(page, features="html.parser")
            sections = soup.find_all('section', class_='items')[1:]
            return sections
            # data_url = soup.find_all('section', class_='items')
        # for i in range(len(data_url)):
        #     news = data_url[i].find_all('div', class_='item')
        #     for p in range(len(news)):
        #         news_item = {}
        #         news_item['category'] = data_url[i].find('h2').text
        #         news_item['title'] = news[p].find('a').text
        #         news_item['url'] = news[p].find('a').get('href')
        #         news_item['source'] = news[p].find('span').text
        #         news_item['time'] = news[p].find('time').text
        #         full_data.append(news_item)
        
        
        #     title = soup.find("h1").text

        #         await file.write(title +"\n")
        # await file.write("\n")

async def get_items_from_section(section_id, section_list):
    items = section_list[section_id].find_all('div', class_='item')
    news_list = []
    for item in items:
        category = section_list[section_id].find('h2').text
        title = item.find('a').text
        url = item.find('a').get('href')
        source = item.find('span').text[1:-1]
        time = item.find('time').text
        news_list.append(get_object(category, title, url, source, time))
        # print(get_object(category, title, url, source, time))
    # print(news_list)
    return news_list
        # get_object(category, title, url, source, time))




def start_parsing():
    section_list = asyncio.run(get_response())
    for id in range(len(section_list)):
        news_list = asyncio.run(get_items_from_section(id+1,section_list))
        print(news_list)

def get_object(category, title, url, source, time):
    return {'category': category, 'title': title, 'url': url, 'source': source, 'time': time}

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
    # main()

    start_parsing()


# count of titles
# get 
#   section: .feed__section (1:)
#       category: .feed__section--title
#       item: .feed__section .feed__item 
#           title: feed__item--title 
#               url: a
#               source: span a
#           time: time

