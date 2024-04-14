import aiohttp
from bs4 import BeautifulSoup
from aiogram import types


async def parse_groups():
    groups = {}
    url = 'http://stud.mephi3.ru/Rasp/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html_code = await response.text()

    soup = BeautifulSoup(html_code, 'html.parser')
    links = soup.find_all('a', class_='dxeHyperlink_MaterialCompact')

    for link in links:
        href = link.get('href')
        group_value = href.split('group=')[1].split('&')[0]
        group_name = link.get_text()
        groups[group_name] = group_value

    return groups



