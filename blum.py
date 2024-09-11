print("Created by lalka2003\n")
print("https://t.me/chad_trade\n" * 3)

import asyncio
import random

import aiohttp

jwt_bearer = "https://telegram.blum.codes/#tgWebAppData=query_id=AAEVr25wAgAAABWvbnDKn-Sb&user={%22id%22:6181269269,%22first_name%22:%22%E2%8F%A4%CD%9F%CD%9E%F0%9D%99%80%F0%9D%99%8D%F0%9D%99%8D%F0%9D%99%8A%F0%9D%99%8D%22,%22last_name%22:%22%22,%22username%22:%22ERR0R9%22,%22language_code%22:%22en%22,%22allows_write_to_pm%22:true}&auth_date=1726039790&hash=b4d2d82980eb0e1afdbc31c72f46a12630c44c99f42186c44fb1c55a50b4ee5f&tgWebAppVersion=7.6&tgWebAppPlatform=android&tgWebAppThemeParams={%22bg_color%22:%22#26293a%22,%22section_bg_color%22:%22#212332%22,%22secondary_bg_color%22:%22#191a26%22,%22text_color%22:%22#ffffff%22,%22hint_color%22:%22#838697%22,%22link_color%22:%22#7d95de%22,%22button_color%22:%22#768fe9%22,%22button_text_color%22:%22#ffffff%22,%22header_bg_color%22:%22#282938%22,%22accent_text_color%22:%22#869eed%22,%22section_header_text_color%22:%22#98aef8%22,%22subtitle_text_color%22:%22#7f838f%22,%22destructive_text_color%22:%22#ee686f%22,%22section_separator_color%22:%22#0f1118%22}"
blum_points_to_claim = [250, 300]


class BlumClient:
    def __init__(
            self,
            bearer: str,
            proxy: str | None = None,
    ) -> None:
        self.bearer = bearer
        self.proxy = proxy
        self.headers = {"Authorization": self.bearer}
        self.session = aiohttp.ClientSession(
            base_url="https://game-domain.blum.codes",
            headers=self.headers,
        )

    async def balance(self) -> dict | None:
        _balance_raw = await self.session.request(
            url="/api/v1/user/balance",
            method="GET",
            proxy=self.proxy,
        )

        _balance: dict = await _balance_raw.json()

        if _balance_raw.status != 200:
            raise Exception(str(_balance))

        return _balance


    async def play(self) -> dict | None:
        _play_raw = await self.session.request(
            url="/api/v1/game/play",
            method="POST",
            proxy=self.proxy,
        )

        _play: dict = await _play_raw.json()

        if _play_raw.status != 200:
            raise Exception(str(_play))

        return _play


    async def claim(self, game_id: str, points: int = 300) -> bool | None:
        _claim_raw = await self.session.request(
            url="/api/v1/game/claim",
            method="POST",
            json={"gameId": game_id, "points": points},
            proxy=self.proxy,
        )

        if _claim_raw.status != 200:
            _claim = await _claim_raw.json()
            raise Exception(str(_claim))

        return True


async def easy_farm(
        jwt_bearer: str,
        blum_points_to_claim: list[int],
) -> None:
    blum_client = BlumClient(jwt_bearer)

    balance = await blum_client.balance()

    available_balance = float(balance.get("availableBalance"))
    game_passes = balance.get("playPasses")

    while game_passes > 0:
        balance = await blum_client.balance()

        available_balance = float(balance.get("availableBalance"))
        game_passes = balance.get("playPasses")

        print(f"BP's:\t\t{available_balance:.2f}")
        print(f"GP's left:\t{game_passes}\n")

        game = await blum_client.play()
        game_id = game.get("gameId")

        print("Game started!")
        print(f"Game ID:\t{game_id}\n")

        print("Waiting for 30 secs..\n")

        await asyncio.sleep(30.00)

        bp_claim_amount = random.randint(
            blum_points_to_claim[0],
            blum_points_to_claim[1],
        )

        claim = await blum_client.claim(game_id, bp_claim_amount)

        if claim:
            print("BP's claimed!")
            print(f"BP's claim:\t{bp_claim_amount}\n")

        print("Sleep for 10 secs..\n")
        await asyncio.sleep(10.00)

    await blum_client.session.close()


if __name__ == "__main__":
    if len(jwt_bearer) == 0:
        jwt_bearer = input("Paste your JWT: ")

    _blum_points_to_claim = input(
        f"Enter BP's amount to claim,"
        f" defaults {blum_points_to_claim[0]}-{blum_points_to_claim[1]} BP's."
        f" Example 100-150 or press enter to skip: ",
    ).split(sep="-")

    if len(_blum_points_to_claim[0]) == 0:
        pass

    if len(_blum_points_to_claim) == 2:
        blum_points_to_claim = []
        [blum_points_to_claim.append(int(amount)) for amount in _blum_points_to_claim]

    asyncio.run(easy_farm(jwt_bearer, blum_points_to_claim))
