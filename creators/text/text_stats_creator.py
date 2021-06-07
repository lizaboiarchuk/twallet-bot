import calendar
import aiohttp
from config import SERVER_URL
from datetime import date
import datetime


async def get_text_stats(chart_query: dict, chat_id):
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
    res = await create_history(start_date, end_date, chat_id)
    return res


async def create_history(start_date, end_date, chat_id):
    result_string = ""
    async with aiohttp.ClientSession() as session:
        data = {}
        data["user_id"] = chat_id
        async with session.get(f'{SERVER_URL}/outcomes', json=data) as resp:
            outcomes = await resp.json()
        async with session.get(f'{SERVER_URL}/incomes', json=data) as resp:
            incomes = await resp.json()

    incomes_category_dict = dict.fromkeys(set([inc['name'] for inc in incomes]), 0)
    outcomes_category_dict = dict.fromkeys(set([out['category'] for out in outcomes]), 0)
    outcomes_names_dict = dict.fromkeys(set([f"{out['category']}_{out['name']}" for out in outcomes]), 0)
    incomes_total = 0
    outcomes_total = 0
    for inc in incomes:
        incomes_total += float(inc['sum'])
        incomes_category_dict[inc['name']] += inc['sum']

    for outc in outcomes:
        outcomes_total += float(outc['sum'])
        outcomes_category_dict[outc['category']] += outc['sum']
        outcomes_names_dict[f"{outc['category']}_{outc['name']}"] += outc['sum']

    result_string += f"Your statistics from {start_date} to {end_date}:\n\n" \
                     f"INCOMES\n" \
                     f"Total = %.2f" % incomes_total + " UAH.\n\n" \
                                                       f"By sources:\n"
    for key in incomes_category_dict:
        perc = ("%.2f" % (incomes_category_dict[key] / incomes_total * 100))
        result_string += key + " - " + str(incomes_category_dict[key]) + " UAH (" + perc + "%)\n"


    result_string +=  f"\n\nEXPENSES\n"
    result_string += f"Total = %.2f" % outcomes_total + " UAH.\n\n" \
                                                        f"By categories:\n"
    for key in outcomes_category_dict:
        perc = ("%.2f" % (outcomes_category_dict[key] / outcomes_total * 100))
        result_string += key + " - " + str(outcomes_category_dict[key]) + " UAH (" + perc + "%)\n"
        for name in outcomes_names_dict:
            if name.startswith(key):
                name_perc = ("%.2f" % (outcomes_names_dict[name] / outcomes_total * 100))
                result_string += "\t" + name.replace(f"{key}_", "") + " - " + str(
                    outcomes_names_dict[name]) + " UAH (" + name_perc + "%)\n"
        result_string+='\n'


    return result_string == "" and "No transactions for this period" or result_string
