from asyncio import run

from x_model import init_db
from xync_schema import models
from xync_schema.models import Ex

from xync_client.Abc.Ex import BaseExClient
from xync_client.loader import PG_DSN


class Client(BaseExClient):
    headers: dict[str, str] = {
        "header1": "значение1",
        "header2": "значение2",
    }

    # 20: order_request
    async def pms(self):
        for cur in await self.curs():
            params = {
                "coinName": "USDT",
                "tradeCoinName": cur,
                "type": "1",
                "amount": "500",
            }
            pms = await self._get("/api/fiat/v1/rapid-buy-integration", params=params)

        return [pm.get("paymentMethod")["name"] for pm in pms["data"]["matchOptimalAdvertListVo"]["optimals"]]

    # 21: order_request_ask
    async def curs(self):
        params = {
            "type": "1",
            "asset": "USDT",
            "coinType": "2",
        }
        curs = await self._get(
            "/api/c2c/v1/common/supportCoins",
            params=params,
        )

        return [i.get("name") for i in curs.json()["data"]["coins"]]

    # 22: cur_pms_map
    async def cur_pms_map(self):
        pass

    # 23: coins
    async def coins(self):
        pass

    # 24: ads
    async def ads(self, coin_exid: str, cur_exid: str, is_sell: bool, pm_exids: list[str | int] = None):
        pass


async def main():
    _ = await init_db(PG_DSN, models, True)
    bg = await Ex.get(name="BingX")
    cl = Client(bg)
    await cl.curs()
    await cl.pms()
    await cl.close()


run(main())
