# -*- coding: utf-8 -*-
from models.Biliapi import BiliWebApi
import json, time

def bili_lottery(data, stime, etime):
    "抽取从stime到etime之间的抽奖，stime<etime"
    try:
        biliapi = BiliWebApi(data)
    except Exception as e: 
        print(f'登录验证id为{data["DedeUserID"]}的账户失败，原因为{str(e)}，跳过后续所有操作')
        return

    print(f'登录账户 ({biliapi.getUserName()}) 成功，开始转发抽奖动态')

    datas = biliapi.getDynamic()
    already_repost_dyid = [] #记录动态列表中自己已经转发的动态id
    try:
        for x in datas:
            if str(x["desc"]["uid"]) == data["DedeUserID"] and x["desc"]["pre_dy_id"]: #记录本账号转发过的动态
                already_repost_dyid.append(x["desc"]["pre_dy_id"])
                continue

            timestamp = x["desc"]["timestamp"]
            if(timestamp > etime):
                continue
            elif(timestamp < stime):
                break
            if 'extension' in x and 'lott' in x["extension"]: #若抽奖标签存在
                uname = x["desc"]["user_profile"]["info"]["uname"]  #动态的主人的用户名
                dyid = x["desc"]["dynamic_id"]
                if dyid in already_repost_dyid: #若动态被转发过就跳过
                    continue
                try:
                    biliapi.repost(dyid)
                    print(f'转发抽奖(用户名:{uname},动态id:{dyid})成功，等待30s')
                    time.sleep(30)
                except Exception as e: 
                    print(f'转发抽奖(用户名:{uname},动态id:{dyid})失败，原因为{str(e)}')
            
    except Exception as e: 
        print(f'获取动态列表、异常，原因为{str(e)}，跳过后续所有操作')
        return

def main(*args):
    now_time = int(time.time()) #当前时间
    time1 = now_time - (now_time + 28800) % 86400 + 43200 #当天中午12点
    time2 = time1 - 86400 #昨天中午12点
    #对time2到time1之间的抽奖动态进行转发

    with open('config/config.json','r',encoding='utf-8') as fp:
        configData = json.load(fp)

    for x in configData["cookieDatas"]:
        bili_lottery(x, time2, time1)

if __name__=="__main__":
    main()
