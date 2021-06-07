import aiohttp
from config import SERVER_URL
from datetime import date
import datetime
import calendar
import os
import plotly.graph_objects as go

from loader import bot


async def date_range(start, end):
    delta = end - start  # as timedelta
    days = [start + datetime.timedelta(days=i) for i in range(delta.days + 1)]
    return days


async def get_chart(chart_query: dict, chat_id):
    if chart_query['Period'].lower() == 'week':
        end_date = date.today()
        delta = datetime.timedelta(weeks=-1)
        start_date = end_date + delta
    elif chart_query['Period'].lower() == 'month':
        end_date = date.today()
        start_month = end_date.month == 1 and 12 or end_date.month - 1
        start_year = start_month == 12 and end_date.year - 1 or end_date.year
        start_day = end_date.day
        last_day_of_month = calendar.monthrange(start_year, start_month)[1]
        if last_day_of_month < end_date.day:
            start_day = last_day_of_month
        start_date = datetime.date(start_year, start_month, start_day)

    elif chart_query['Period'].lower() == 'year':
        end_date = date.today()
        start_year = end_date.year - 1
        start_day = end_date.day
        last_day_of_month = calendar.monthrange(start_year, end_date.month)[1]
        if last_day_of_month < end_date.day:
            start_day = last_day_of_month
        start_date = datetime.date(start_year, end_date.month, start_day)

    if chart_query['Kind'] == 'pie chart':
        await get_pie_chart(start_date, end_date, chat_id)
    elif chart_query['Kind'] == 'column chart':
        await get_gist_chart(start_date, end_date, chat_id)


async def prepare_data_outcomes(start_date, end_date, chat_id: int):
    dt_range = await date_range(start_date, end_date)
    async with aiohttp.ClientSession() as session:
        data = {}
        data["user_id"] = chat_id
        async with session.get(f'{SERVER_URL}/outcomes', json=data) as resp:
            res = await resp.json()
    filtered_outcomes = []
    for outcome in res:
        out_date_tokens = outcome['date'].split('/')
        out_date = datetime.date(int(out_date_tokens[2]), int(out_date_tokens[1]), int(out_date_tokens[0]))
        if out_date in dt_range:
            filtered_outcomes.append(outcome)

    values = set(map(lambda x: x['category'], filtered_outcomes))
    values.add('other')

    summary = [[y['sum'] for y in filtered_outcomes if y['category'] == x] for x in values]
    categories_summary = [list(map(sum, summary))][0]
    values = list(map(lambda x: str(x).capitalize(), values))
    dict_cat = dict(zip(values, categories_summary))
    copy_dict = dict_cat.copy()
    for key in copy_dict:
        if dict_cat[key] == 0:
            dict_cat.pop(key)
    return dict_cat


async def prepare_data_incomes(start_date, end_date, chat_id: int):
    dt_range = await date_range(start_date, end_date)
    async with aiohttp.ClientSession() as session:
        data = {}
        data["user_id"] = chat_id
        async with session.get(f'{SERVER_URL}/incomes', json=data) as resp:
            res = await resp.json()
    filtered_incomes = []
    for income in res:
        in_date_tokens = income['date'].split('/')
        in_date = datetime.date(int(in_date_tokens[2]), int(in_date_tokens[1]), int(in_date_tokens[0]))
        if in_date in dt_range:
            filtered_incomes.append(income)

    values = set(map(lambda x: x['name'], filtered_incomes))
    values.add('other')

    summary = [[y['sum'] for y in filtered_incomes if y['name'] == x] for x in values]
    source_summary = [list(map(sum, summary))][0]
    values = list(map(lambda x: str(x).capitalize(), values))
    dict_cat = dict(zip(values, source_summary))
    copy_dict = dict_cat.copy()
    for key in copy_dict:
        if dict_cat[key] == 0:
            dict_cat.pop(key)
    return dict_cat


async def get_pie_chart(start_date, end_date, chat_id: int):
    dict_cat = await prepare_data_outcomes(start_date, end_date, chat_id)
    fig = go.Figure(
        data=[go.Pie(values=list(dict_cat.values()), labels=list(dict_cat.keys()))])
    fig.update_layout(title='Expenses by categories')
    fig.write_image(f'outputs/chart_pie_{chat_id}.png')

    dict_incomes = await prepare_data_incomes(start_date, end_date, chat_id)
    fig = go.Figure([go.Pie(labels=list(dict_incomes.keys()), values=list(dict_incomes.values()))])
    fig.update_layout(title='Incomes by sources')
    fig.write_image(f'outputs/chart_pie_inc_{chat_id}.png')

    await bot.send_document(chat_id=chat_id, document=open(f'outputs/chart_pie_{chat_id}.png', 'rb'))
    await bot.send_document(chat_id=chat_id, document=open(f'outputs/chart_pie_inc_{chat_id}.png', 'rb'))

    if os.path.exists(f"outputs/chart_pie_{chat_id}.png"):
        os.remove(f"outputs/chart_pie_{chat_id}.png")
    if os.path.exists(f"outputs/chart_pie_inc_{chat_id}.png"):
        os.remove(f"outputs/chart_pie_inc_{chat_id}.png")


async def get_gist_chart(start_date, end_date, chat_id: int):
    dict_cat = await prepare_data_outcomes(start_date, end_date, chat_id)
    fig = go.Figure([go.Bar(x=list(dict_cat.keys()), y=list(dict_cat.values()))])
    fig.update_layout(title='Expenses by categories')
    fig.write_image(f'outputs/chart_bar_{chat_id}.png')

    dict_incomes = await prepare_data_incomes(start_date, end_date, chat_id)
    fig = go.Figure([go.Bar(x=list(dict_incomes.keys()), y=list(dict_incomes.values()))])
    fig.update_layout(title='Incomes by sources')
    fig.write_image(f'outputs/chart_bar_inc_{chat_id}.png')

    await bot.send_document(chat_id=chat_id, document=open(f'outputs/chart_bar_inc_{chat_id}.png', 'rb'))
    await bot.send_document(chat_id=chat_id, document=open(f'outputs/chart_bar_{chat_id}.png', 'rb'))

    if os.path.exists(f"outputs/chart_bar_inc_{chat_id}.png"):
        os.remove(f"outputs/chart_bar_inc_{chat_id}.png")
    if os.path.exists(f"outputs/chart_bar_{chat_id}.png"):
        os.remove(f"outputs/chart_bar_{chat_id}.png")
