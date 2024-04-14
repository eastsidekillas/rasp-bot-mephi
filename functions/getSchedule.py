import aiohttp
from bs4 import BeautifulSoup


async def get_schedule(group_id):
    group = group_id.replace('_', '')
    url = f"http://stud.mephi3.ru/Rasp/Rasp.aspx?group={group}&sem=2"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html_code = await response.text()

    soup = BeautifulSoup(html_code, 'html.parser')
    schedule_info = soup.find_all('tr', class_='dxgvDataRow_MaterialCompact')
    schedule = []
    for info in schedule_info:
        time = info.find('td', class_='dx-nowrap dxgv dx-ac').get_text(strip=True)
        subject = info.find_all('td', class_='dxgv dx-ac')[0].get_text(strip=True)
        lecturer_and_auditorium = info.find_all('td', class_='dxgv dx-ac')[1].find_all('br')

        if len(lecturer_and_auditorium) == 2:
            lecturer, auditorium = map(lambda x: x.get_text(strip=True), lecturer_and_auditorium)
        elif len(lecturer_and_auditorium) == 1:
            lecturer = lecturer_and_auditorium[0].get_text(strip=True)
            auditorium = ''  # Установите значение по умолчанию, если аудитория не указана
        else:
            # Обработайте ситуацию, если количество <br> не равно 1 или 2
            print(f"Unexpected number of <br> elements: {len(lecturer_and_auditorium)}")
            continue

        start_time, end_time = map(str.strip, time.split('<br>'))
        schedule.append({
            'start_time': start_time,
            'end_time': end_time,
            'subject': subject,
            'lecturer': lecturer,
            'auditorium': auditorium
        })

    return schedule

