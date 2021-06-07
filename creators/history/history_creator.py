import aiohttp
from config import SERVER_URL
from datetime import date
import datetime
from utils.currency_codes import CURRENCY_NAMES


async def date_range(start, end):
    delta = end - start  # as timedelta
    days = [start + datetime.timedelta(days=i) for i in range(delta.days + 1)]
    return days


async def get_history(hist_query: dict, chat_id):
    if hist_query['Period'].lower() == 'other':
        start_tokens = hist_query['date_start'].split('/')
        start_date = datetime.date(int(start_tokens[2]), int(start_tokens[1]), int(start_tokens[0]))
        end_tokens = hist_query['date_end'].split('/')
        end_date = datetime.date(int(end_tokens[2]), int(end_tokens[1]), int(end_tokens[0]))

    elif hist_query['Period'].lower() == 'week':
        end_date = date.today()
        delta = datetime.timedelta(weeks=-1)
        start_date = end_date + delta

    elif hist_query['Period'].lower() == 'day':
        end_date = date.today()
        delta = datetime.timedelta(days=0)
        start_date = end_date + delta

    res = ""
    if hist_query['Type'].lower() == 'incomes':
        res = await incomes_history(start_date, end_date, chat_id)


    elif hist_query['Type'].lower() == 'expenses':
        res = await outcomes_history(start_date, end_date, chat_id)


    elif hist_query['Type'].lower() == 'all':
        res = await all_history(start_date, end_date, chat_id)

    return res


async def incomes_history(start_date, end_date, chat_id):
    dt_range = await date_range(start_date, end_date)
    async with aiohttp.ClientSession() as session:
        data = {}
        data["user_id"] = chat_id
        async with session.get(f'{SERVER_URL}/incomes', json=data) as resp:
            res = await resp.json()
    filtered_incomes = []
    for income in res:
        inc_date_tokens = income['date'].split('/')
        inc_date = datetime.date(int(inc_date_tokens[2]), int(inc_date_tokens[1]), int(inc_date_tokens[0]))
        if inc_date in dt_range:
            filtered_incomes.append(income)
    result_string = ""
    filtered_incomes.sort(key=lambda x: datetime.date(int(x['date'].split('/')[2]), int(x['date'].split('/')[1]),
                                                      int(x['date'].split('/')[0])))
    for income in filtered_incomes:
        print(income)
        result_string += income['date'] + " - " + str(income['sum']) + " " + "UAH" + " (" + income['name'] + ")" + '\n'
    return result_string == "" and "No incomes for this period" or result_string


async def outcomes_history(start_date, end_date, chat_id):
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
    result_string = ""
    filtered_outcomes.sort(key=lambda x: datetime.date(int(x['date'].split('/')[2]), int(x['date'].split('/')[1]),
                                                       int(x['date'].split('/')[0])))
    for outcome in filtered_outcomes:
        print(outcome)
        result_string += outcome['date'] + " - " + str(outcome['sum']) + " " + "UAH" + " (" + outcome['category'] + ")" + '\n'
    return result_string == "" and "No outcomes for this period" or result_string





async def all_history(start_date, end_date, chat_id):
    dt_range = await date_range(start_date, end_date)
    async with aiohttp.ClientSession() as session:
        data = {}
        data["user_id"] = chat_id
        async with session.get(f'{SERVER_URL}/outcomes', json=data) as resp:
            outcomes = await resp.json()
        async with session.get(f'{SERVER_URL}/incomes', json=data) as resp:
            incomes = await resp.json()

    outcomes.extend(incomes)
    all_comes = outcomes
    filtered_items = []
    for it in all_comes:
        date_tokens = it['date'].split('/')
        all_date = datetime.date(int(date_tokens[2]), int(date_tokens[1]), int(date_tokens[0]))
        if all_date in dt_range:
            filtered_items.append(it)
    result_string = ""
    filtered_items.sort(key=lambda x: datetime.date(int(x['date'].split('/')[2]), int(x['date'].split('/')[1]),
                                                       int(x['date'].split('/')[0])))

    print(filtered_items)
    for it in filtered_items:
        print(it)

        if 'category' in it:
            result_string += "EXPENSE.  " + it['date'] + " - " + str(it['sum']) + " " + "UAH" + " (" + it['category'] + ")" + '\n'
        else:
            result_string += "INCOME.  " + it['date'] + " - " + str(it['sum']) + " " + "UAH" + " (" + it['name'] + ")" + '\n'
    return result_string == "" and "No transactions for this period" or result_string


