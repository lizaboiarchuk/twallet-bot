import calendar
import aiohttp
from config import SERVER_URL
from datetime import date
import datetime
import xlsxwriter
from loader import bot
import os

async def get_xlsx_stats(chart_query: dict, chat_id):
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
    await create_history(start_date, end_date, chat_id)


async def create_history(start_date, end_date, chat_id):
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

    workbook = xlsxwriter.Workbook(f'outputs/stats_{chat_id}.xlsx')
    incomes_worksheet = workbook.add_worksheet("Incomes")
    row = 0
    column = 0
    for key in incomes_category_dict:
        incomes_worksheet.write(row, column, key)
        incomes_worksheet.write(row, column + 1, str(incomes_category_dict[key]))
        perc = ("%.2f" % (incomes_category_dict[key] / incomes_total * 100))
        incomes_worksheet.write(row, column + 2, f"{perc}%")
        row += 1
    incomes_worksheet.write(row, column, "TOTAL")
    incomes_worksheet.write(row, column + 1, f"%.2f" % incomes_total)

    outcomes_worksheet = workbook.add_worksheet('Expenses')
    row = 0
    column = 0
    for key in outcomes_category_dict:
        outcomes_worksheet.write(row, column, key)
        outcomes_worksheet.write(row, column + 2, str(outcomes_category_dict[key]))
        perc = ("%.2f" % (outcomes_category_dict[key] / outcomes_total * 100))
        outcomes_worksheet.write(row, column + 3, f"{perc}%")
        row += 1
        for name in outcomes_names_dict:
            if name.startswith(key):
                name_perc = ("%.2f" % (outcomes_names_dict[name] / outcomes_total * 100))
                outcomes_worksheet.write(row, column + 1, name.replace(f"{key}_", ""))
                outcomes_worksheet.write(row, column + 2, str(outcomes_names_dict[name]))
                outcomes_worksheet.write(row, column + 3, f"{name_perc}%")
                row += 1
    outcomes_worksheet.write(row, column, "TOTAL")
    outcomes_worksheet.write(row, column + 2, f"%.2f" % incomes_total)
    workbook.close()

    await bot.send_document(chat_id=chat_id, document=open(f'outputs/stats_{chat_id}.xlsx', 'rb'))

    if os.path.exists(f"outputs/stats_{chat_id}.xlsx"):
        os.remove(f"outputs/stats_{chat_id}.xlsx")





