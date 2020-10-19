BiliExp-Actions
====  
##### 本分支为主分支的云函数功能的一部分，去除了对云函数的依赖，只需要github Actions就能使用，最新功能在本分支更新，因此会频繁变动，如无必要可以不及时更新代码(除非出现严重bug)

[![](https://img.shields.io/badge/author-%E6%98%9F%E8%BE%B0-red "作者")](https://github.com/happy888888/ )
![](https://img.shields.io/badge/dynamic/json?label=GitHub%20Followers&query=%24.data.totalSubs&url=https%3A%2F%2Fapi.spencerwoo.com%2Fsubstats%2F%3Fsource%3Dgithub%26queryKey%3Dhappy888888&labelColor=282c34&color=181717&logo=github&longCache=true "关注数量")
![](https://img.shields.io/github/stars/happy888888/BiliExp.svg?style=plastic&logo=appveyor "Star数量")
![](https://img.shields.io/github/forks/happy888888/BiliExp.svg?style=plastic&logo=stackshare "Fork数量")

### 主要功能
**B站自动操作脚本**
* [x] 自动获取经验(投币、点赞、分享视频) 
* [x] 自动转发互动抽奖并评论(自己关注的up主,支持指定关键字如"#互动抽奖#")
* [x] 参与官方转盘抽奖活动(activity，目前没有自动搜集活动的功能,需要在config/activity.json里面手动指定)
* [x] 直播辅助(直播签到，~~直播挂机~~，直播自动送出快过期礼物) 
* [x] 自动兑换银瓜子为硬币 
* [x] 自动领取大会员每月权益(B币劵，优惠券)(每月1号) 
* [x] 自动将大会员B币劵给自己账户充电。(每月28号)
* [x] 漫画辅助脚本(漫画APP签到，自动花费即将过期漫读劵，自动积分兑换漫画福利券，自动领取大会员每月福利劵，自动参加每月"站友日"活动) 
* [x] 定时清理无效动态(转发的过期抽奖，失效动态，支持自定义关键字，非官方渠道抽奖无法判断是否过期) 
* [ ] ~~直播开启宝箱领取银瓜子(本活动已结束，不知道B站以后会不会再启动)~~ 
* [x] 风纪委员投票(处于功能测试状态，目前每次执行只投一次票)
</br>

```
如有其他功能需求请发issue，提供功能说明和功能所在的B站页面(app功能可提供界面截图和进入方式)以及分支名称(BiliExp-Actions)
```

### 使用方式
* 1. 准备
    *  1.1 一个或多个B站账号，以及登录后获取的SESSDATA，bili_jct，DedeUserID (获取方式见最下方示意图)
    *  1.2 fork本项目
* 2. 简单部署(与3.复杂部署二选一)
    *  2.1 在fork后的github仓库的 “Settings” --》“Secrets” 中添加"Secrets"，name和value分别为：
        *  2.1.1 name为"biliconfig"           value为B站账号登录信息，格式如下
        ```
        SESSDATA
        bili_jct
        uid
        ```
        例如下面这样
        ```
        e1272654%vfdawi241825%2C8dc06*a1
        0a9081cc53856314783d195f5ddbadf3
        203953353
        ```
        ![image](https://user-images.githubusercontent.com/67217225/95849036-77654580-0d81-11eb-8125-9adcd23ec25a.png)
    *  2.2 添加完上面的"Secrets"后，进入"Actions" --》"run BiliExp"，点击右边的"Run workflow"即可第一次启动
        *  2.2.1 首次fork可能要去actions(正上方的actions不是Settings里面的actions)里面同意使用actions条款，如果"Actions"里面没有"run BiliExp"，点一下右上角的"star"，"run BiliExp"就会出现在"Actions"里面
        *  2.2.2 第一次启动后，脚本会每天12:00自动执行，不需要再次手动执行(第一次手动执行这个步骤不能忽略)。
        ```
        注: 本部署方式仅提供默认配置，功能的详细配置包括但不限于以下所列，请使用下面的复杂部署方式
		1. 自定义功能开启与关闭(简单部署不开启所有功能)
		2. 投币功能自定义投币数量(简单部署默认为5，达到6级后第二天停止)
		3. 抽奖动态转发自定义评论内容，简单部署默认评论为(从未中奖，从未放弃[doge])
		4. 漫画辅助功能的启用与详细配置，简单部署不启用此功能
		5. 风纪委员投票功能的启用与详细配置，简单部署不启用此功能
		6. 多账户的支持(支持50个以上的B站账号)，简单部署只能单账号
        ```
        
* 3. 复杂部署与本地部署(与2.简单部署二选一)
    *  3.1 进入config文件夹，按照说明配置config.json文件
    *  3.2 在fork后的github仓库的 “Settings” --》“Secrets” 中添加"Secrets"，name和value分别为：
        *  3.2.1 name为"advconfig"(注意不是上面的biliconfig)     value为3.1步骤配置好的config.json文件(直接把整个文件复制到这里)
    *  3.3 同上面2.2配置
    ```
        advconfig设置后不需要设置biliconfig
        需要本地运行则直接配置config/config.json文件并运行BiliExp.py即可(必须安装依赖aiohttp，可以执行pip3 install aiohttp)
    ```

</br>

### 2020/10/19更新

* 1.修复部分动态转发问题
* 2.调整模块名

### 2020/10/16更新

* 1.增加风纪委员投票的功能

</br></br>

### 2020/10/13更新

* 1.调整代码结构，程序改为单入口
* 2.用aiohttp重写B站接口类，整个脚本改用协程并发执行提高效率(activity单ip地址五秒内只能请求一次只能加锁限制并发)
* 3.将功能模块化，通过配置文件控制模块的加载和开关

</br></br>


### 2020/10/01更新

* 1.主分支的更新内容
* 2.官方转盘抽奖活动的活动列表改为手动指定，存放在config/activity.json(自动搜索活动的效率太低)

</br></br>

### 2020/09/27更新

* 1.互动抽奖方式改为转发并评论(听说能提高中奖率🤑🤩)。

</br></br>

### 2020/09/26更新

* 1.增加email推送。

</br></br>

### 2020/09/24更新

* 1.移除参加B站活动抽奖的脚本的活动列表文件，改为自动获取。(现在这个活动抽奖很鸡肋)

</br></br>


B站操作需要的cookie数据可以按照以下方式获取
浏览器打开B站主页--》按F12打开开发者工具--》application--》cookies
<div align="center"><img src="https://s1.ax1x.com/2020/09/23/wjM09e.png" width="800" height="450" title="获取cookies示例"></div>
