import status_client_support
from frontend import Menager
from server import Client, Game
import asyncio


async def play_game(game: Game):
    menager = Menager()

    try:
        await game.run
    except status_client_support.Errors_game as e:
        menager.push_status(None, error=e)


async def run(self):

    client = Client()
    menager = Menager()

    while True:
        await asyncio.sleep(0.01)
        messege = menager.pop_messange()
        if not isinstance(messege, tuple):
            menager.push_status(
                None, error=status_client_support.Errors_game("", 1))
            continue

        match messege[0]:
            case 0:
                break
            case 1:
                game = client.connect_game(messege[1])
            case code if 1 < code < len(status_client_support._STATUS_):
                game_name = messege[1][22:]
                game = client.init_game(game_name)
            case _:
                menager.push_status(
                    None, error=status_client_support.Errors_game("", 1))
                continue

        await play_game(game)
