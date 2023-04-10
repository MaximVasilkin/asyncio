from asyncio import run, gather, create_task, all_tasks, current_task
from aiohttp import ClientSession
from math import ceil
from work_with_db import paste_to_db
from loop_policy import check_loop_policy


check_loop_policy()

URL = 'https://swapi.dev/api/people/'


async def get_json(client, *args, **kwargs):
    response = await client.get(*args, **kwargs)
    json_ = await response.json()
    return json_


async def get_page_meta():
    async with ClientSession() as client:
        info = await get_json(client, URL)
        persons_on_page = len(info['results'])
        all_persons_num = info['count']
        max_page_num = ceil(all_persons_num / persons_on_page)
        return max_page_num, persons_on_page


MAX_PAGE_COUNT, PERSONS_ON_PAGE = run(get_page_meta())


async def get_listed_data(client, field: str, *links):
    if not links:
        return
    coroutines = [get_json(client, link) for link in links]
    jsons = await gather(*coroutines)
    data = ', '.join(json_[field] for json_ in jsons)
    return data


async def get_person_data(client, person, id_):

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

    return person_data


async def get_persons_from_page(client, page: int):
    params = {'page': page}
    start_position = (page * PERSONS_ON_PAGE) - (PERSONS_ON_PAGE - 1)
    response = await get_json(client, URL, params=params)
    persons = [await get_person_data(client, person, id_) for id_, person in enumerate(response['results'],
                                                                                       start=start_position)]
    return persons


async def get_all_persons():
    async with ClientSession() as client:
        for page in range(1, MAX_PAGE_COUNT + 1):
            persons = await get_persons_from_page(client, page)
            paste_to_db_coroutine = paste_to_db(persons)
            create_task(paste_to_db_coroutine)
        tasks = all_tasks() - {current_task(), }
        for task in tasks:
            await task


if __name__ == '__main__':
    run(get_all_persons())
