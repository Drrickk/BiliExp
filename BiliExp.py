# -*- coding: utf-8 -*-
import asyncio, json, time, logging, sys, re, io
from models.asyncBiliApi import asyncBiliApi
#from tasks import * #所有任务模块通过动态加载

log_stream = io.StringIO()

def push_message(SCKEY=None,
                 email=None
                 ) -> None:
    if not (SCKEY or email):
        return

    log = log_stream.getvalue()
    import urllib
    if SCKEY:
        data_string = urllib.parse.urlencode({"text": "B站经验脚本消息推送","desp": log})
        urllib.request.urlopen(f'https://sc.ftqq.com/{SCKEY}.send', data=data_string.encode())
    if email:
        data_string = urllib.parse.urlencode({"email":email, "name": "B站经验脚本消息推送","certno": log.replace("\n","<br>")})
        urllib.request.urlopen(f'http://liuxingw.com/api/mail/api.php?{data_string}')

async def run_user_tasks(user,           #用户配置
                        default          #默认配置
                        ) -> None:

    async with asyncBiliApi() as biliapi:
        try:
            if not await biliapi.login_by_cookie(user["cookieDatas"]):
                logging.warning(f'id为{user["cookieDatas"]["DedeUserID"]}的账户cookie失效，跳过此账户后续操作')
                return
        except Exception as e: 
            logging.warning(f'登录验证id为{user["cookieDatas"]["DedeUserID"]}的账户失败，原因为{str(e)}，跳过此账户后续操作')
            return

        tasks = []

        for task in default: #遍历任务列表，把需要运行的任务添加到tasks
            if isinstance(default[task], bool):
                if task in user["tasks"]:
                    if user["tasks"][task]:
                        task_module = __import__(f'tasks.{task}') #载入任务模块
                        task_function = getattr(getattr(task_module, task), task)#载入任务入口方法
                        tasks.append(task_function(biliapi))               #放进任务列表
                elif default[task]:
                    task_module = __import__(f'tasks.{task}')
                    task_function = getattr(getattr(task_module, task), task)
                    tasks.append(task_function(biliapi))
            elif isinstance(task, dict):
                if task in user["tasks"]:
                    if user["tasks"][task]["enable"]:
                        task_module = __import__(f'tasks.{task}')
                        task_function = getattr(getattr(task_module, task), task)
                        tasks.append(task_function(biliapi, user["tasks"][task]))
                elif default[task]["enable"]:
                    task_module = __import__(f'tasks.{task}')
                    task_function = getattr(getattr(task_module, task), task)
                    tasks.append(task_function(biliapi, default[task]))
        if tasks:
            await asyncio.wait(tasks)        #异步等待所有任务完成

def initlog(log_file_name):
    '''初始化日志参数'''
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_file_name)
    console_handler = logging.StreamHandler(stream=sys.stdout)
    strio_handler = logging.StreamHandler(stream=log_stream)
    formatter1 = logging.Formatter("[%(levelname)s]; %(message)s")
    formatter2 = logging.Formatter("%(message)s")
    file_handler.setFormatter(formatter1)
    console_handler.setFormatter(formatter1)
    strio_handler.setFormatter(formatter2)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.addHandler(strio_handler)

def main(*args):
    try:
        initlog("BiliExp.log")
    except:
        print(f'日志配置异常，原因为{str(e)}')

    try:
        with open('config/config.json','r',encoding='utf-8') as fp:
            configData = json.loads(re.sub(r'\/\*[\s\S]*?\/', '', fp.read()))
    except Exception as e: 
        logging.error(f'配置加载异常，原因为{str(e)}，退出程序')
        sys.exit(6)
    
    #启动任务
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(run_user_tasks(user, configData["default"])) for user in configData["users"]]
    loop.run_until_complete(asyncio.wait(tasks))

    try:
        push_message(configData["SCKEY"], configData["email"])
    except Exception as e: 
        logging.error(f'消息推送异常，原因为{str(e)}')

__name__=="__main__" and main()
