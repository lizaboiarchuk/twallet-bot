from aiogram.dispatcher.filters.state import StatesGroup, State

class ShowStats(StatesGroup):
    type = State()

class DiagramStats(StatesGroup):
    period = State()

class TestStats(StatesGroup):
    period = State()

class FileStats(StatesGroup):
    period = State()
