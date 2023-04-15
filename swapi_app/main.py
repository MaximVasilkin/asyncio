from asyncio import run, gather, create_task, all_tasks, current_task
from aiohttp import ClientSession
from math import ceil
from work_with_db import paste_to_db
from datetime import datetime


URL = 'https://swapi.dev/api/people/'


async def get_json(client, *args, **kwargs):
    response = await client.get(*args, **kwargs)
    json_ = await response.json()
    return json_


async def get_page_meta():
    async with ClientSession() as client:
        info = await get_json(client, URL)
        all_persons_num = info['count']
        return all_persons_num


async def get_listed_data(client, field: str, *links):
    if not links:
        return
    coroutines = [get_json(client, link) for link in links]
    jsons = await gather(*coroutines)
    data = ', '.join(json_[field] for json_ in jsons)
    return data


async def get_person_and_paste_to_db(client, id_):
    url = f'{URL}{id_}'
    person = await get_json(client, url)

    if 'detail' in person:
        return

    extra_data = await gather(get_listed_data(client, 'name', person['homeworld']),
                              get_listed_data(client, 'title', *person['films']),
                              get_listed_data(client, 'name', *person['species']),
                              get_listed_data(client, 'name', *person['starships']),
                              get_listed_data(client, 'name', *person['vehicles']))

    person_data = dict(id=id_,
                       birth_year=person['birth_year'],
                       eye_color=person['eye_color'],
                       gender=person['gender'],
                       hair_color=person['hair_color'],
                       height=person['height'],
                       mass=person['mass'],
                       name=person['name'],
                       skin_color=person['skin_color'],
                       homeworld=extra_data[0],
                       films=extra_data[1],
                       species=extra_data[2],
                       starships=extra_data[3],
                       vehicles=extra_data[4])

    await paste_to_db(person_data)


async def get_all_persons():
    async with ClientSession() as client:
        all_persons_num = await get_page_meta()
        for person_id in range(1, all_persons_num + 2):
            person_coro = get_person_and_paste_to_db(client, person_id)
            create_task(person_coro)
        tasks = all_tasks() - {current_task(), }
        for task in tasks:
            await task


if __name__ == '__main__':
    start = datetime.now()
    run(get_all_persons())
    end = datetime.now()
    print(end - start)
