from models.asyncBiliApi import asyncBiliApi
import logging

async def xliveSign_task(biliapi: asyncBiliApi) -> None:
    try:
        ret = await biliapi.xliveSign()
        logging.info(f'{biliapi.name}: bilibili直播签到信息：{ret["message"]}')
    except Exception as e:
        logging.warning(f'{biliapi.name}: 直播签到异常，原因为{str(e)}')