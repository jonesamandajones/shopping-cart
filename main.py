import asyncio

from src.controllers.menu import menu_crud

loop = asyncio.get_event_loop()

loop.run_until_complete(menu_crud())
