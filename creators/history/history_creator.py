import aiohttp
from config import SERVER_URL
from datetime import date
import datetime

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

    for i in range(len(filtered_incomes)):
        for j in range(len(filtered_incomes)):
            inc = filtered_incomes[i]
            i_tokens = inc['date'].split('/')
            i_date = datetime.date(int(i_tokens[2]), int(i_tokens[1]), int(i_tokens[0]))

            inc =  filtered_incomes[j]
            j_tokens = inc['date'].split('/')
            j_date = datetime.date(int(j_tokens[2]), int(j_tokens[1]), int(j_tokens[0]))

            if i_date < j_date:
                temp = filtered_incomes[i]
                filtered_incomes[i] = filtered_incomes[j]
                filtered_incomes[j] = temp

    for income in filtered_incomes:
        print(income)
        result_string+= income['date'] + " - " + str(income['sum']) + " " + str(income['currency']) + " (" + income['name'] + ")" + '\n'

    return result_string








async def outcomes_history(start_date, end_date, chat_id):
    pass




async def all_history(start_date, end_date, chat_id):
    pass

































#     delta = datetime.timedelta(days=1)
#     if hist_query['Period'].lower() == 'day':
#         delta = datetime.timedelta(days=1)
#     elif hist_query['Period'].lower() == 'week':
#         delta = datetime.timedelta(weeks=1)
#     elif hist_query['Period'].lower() == 'month':
#
#         today = date.today()
#         year = today.month == 1 and today.year - 1 or today.year
#         month = today.month == 1 and 12 or today.month-1
#         # day =
#
#         start = datetime.datetime(today.month == 1 and today.year - 1 or today.year, today.month == 1 and 12 or today.month-1, )
#
#
#
#         delta = datetime.da
#     elif hist_query['Yaer'].lower() == 'year':
#         days_num = 364
#
#     if hist_query['Type'].lower() == 'incomes':
#         await incomes_history(period=days_num, chat_id=chat_id)
#     elif hist_query['Type'].lower() == 'outcomes':
#         await outcomes_history(period=days_num, chat_id=chat_id)
#     elif hist_query['Type'].lower() == 'all':
#         await all_history(period=days_num, chat_id=chat_id)
#
#
# async def incomes_history(period: int, chat_id):
#     async with aiohttp.ClientSession() as session:
#         data = {}
#         data["user_id"] = chat_id
#         async with session.get(f'{SERVER_URL}/incomes', json=data) as resp:
#             res = await resp.json()
#
#         today = date.today().strftime("%d/%m/%Y").split('/')
#         days = int(today[0]) + int(int(today[1])*30.5) + int(today[2])*364
#
#         filtered_incomes = []
#         for income in res:
#             income_tokens = income['date'].split('/')
#             income_days = int(income_tokens[0]) + int(int(income_tokens[1])*30.5) + int(income_tokens[2])*364
#             if (income_days) < days and (income_days > days - period):
#                 filtered_incomes.append(income)
#
#
#
#         sorted_incomes = sorted(filtered_incomes, key=lambda x: get_date(x), reverse=True)
#         print(sorted_incomes)
#
#
#
#
#
#
#
#
#
#
#
#
# async def outcomes_history(period: int, chat_id):
#     pass
#
#
# async def all_history(period: int, chat_id):
#     pass
#
#
#
#
#
#
#
# def get_date(income):
#     inc_tokens = income['date'].split('/')
#     inc = datetime.datetime(int(inc_tokens[2]), int(inc_tokens[1]), int(inc_tokens[0]))
#     return inc
#
#
#



