from platform import system
from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy


def check_loop_policy():
    os = system()
    if os == 'Windows':
        set_event_loop_policy(WindowsSelectorEventLoopPolicy())
