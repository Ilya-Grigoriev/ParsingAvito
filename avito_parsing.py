import asyncio
import json
from datetime import datetime
from pyppeteer import launch
from bs4 import BeautifulSoup


async def main(query: str, page_n: int) -> None:
    browser = await launch()
    # browser = await launch({"headless": False, "args": ["--start-maximized"]})
    page = await browser.newPage()
    json_file = open('items.json', encoding='utf-8', mode='w')
    data = []
    for page_n in range(1, page_n + 1):
        await page.goto(f'https://www.avito.ru?p={page_n}&q={query}')
        bs = BeautifulSoup(await page.content(), 'html.parser')
        items = bs.find_all('div', attrs={'data-marker': 'item'})
        sample = 'https://www.avito.ru'
        for item in items:
            title = item.find('h3').get_text()
            url = item.find('a').get_attribute_list('href')
            if url:
                total_url = sample + url[0]
                print(f'Title: {title}')
                print(f'URL: {total_url}')
                data.append({'title': title, 'url': total_url})
    json.dump(data, json_file)
    await browser.close()


if __name__ == '__main__':
    query = input('Введите название товара: ')
    page_n = int(input('Введите количество страниц: '))
    start_time = datetime.now()
    loop = asyncio.new_event_loop()
    asyncio.run(main(query, page_n))
    end_time = datetime.now()
    print(f'Execution time: {end_time - start_time}')
