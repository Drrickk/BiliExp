# -*- coding: utf-8 -*-
from models.Biliapi import BiliWebApi
import time, json

def hiddenUname(uname: str):
    '''替换用户名中一部分为星号'''
    _xlen = len(uname) // 2
    _s = (_xlen + 1) // 2
    return f'{uname[0:_s]}{"*"*_xlen}{uname[_s+_xlen:]}'

def get_activity_lottery():
    '''获取B站活动抽奖id，生成器'''
    import requests
    import re
    session = requests.session()
    pat = re.compile('lotteryId\\\":\\\"(.*?)\\"', re.S)
    def get_id(url):
        text = session.get(f'https:{url}').text
        return re.findall(pat, text)[0]

    list = BiliWebApi.activityList()
    for x in list:
        try:
            yield (x["name"], get_id(x["h5_url"]))
        except:
            pass
    session.close()

def do_activity(cookieData, activity_data):
    try:
       biliapi = BiliWebApi(cookieData)
    except Exception as e:
       print(f'登录验证id为{cookieData["DedeUserID"]}的账户失败，原因为({str(e)})，跳过此账户后续所有操作')
       return
    print(f'账户({hiddenUname(biliapi.getUserName())})开始参与活动抽奖')
    for x in activity_data:
        print(f'开始参与 "{x[0]}" 活动')
        try:
            biliapi.activityAddTimes(x[1], 3) #执行增加抽奖次数操作
            biliapi.activityAddTimes(x[1], 4)
        except Exception as e:
            print(f'增加抽奖次数异常,原因为({str(e)})')

        try:
            times = biliapi.activityMyTimes(x[1])["data"]["times"]
        except Exception as e:
            print(f'获取剩余抽奖次数异常，原因为({str(e)})，在尝试执行1次抽奖')
            times = 1
        else:
            print(f'活动可参与的次数为{times}')

        for ii in range(times):
            try:
                result = biliapi.activityDo(x[1], 1)
                print(f'{ii + 1}.', end="")
                if result["code"]:
                    print(result["message"])
                else:
                    print(result["data"][0]["gift_name"]) #获取奖品名称，目前没发现一次中几个奖的，但是抽奖结果是数组
                    time.sleep(5.5) #抽奖延时
            except Exception as e:
                print(f'参与活动异常，原因为({str(e)})')

def main(*args):
    with open('config/config.json','r',encoding='utf-8') as fp:
        configData = json.load(fp)

    activity_data = list(get_activity_lottery())

    for x in configData["cookieDatas"]:
        do_activity(x, activity_data)

if __name__=="__main__":
    main()