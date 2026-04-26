import asyncio
from lib.menu import run as front
from lib.backend import run as back


async def main():
    """запуск бэка и фронта"""
    await asyncio.gather(
        front(),
        back()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Чтобы не вылетало ошибок при нажатии Ctrl+C
        pass
