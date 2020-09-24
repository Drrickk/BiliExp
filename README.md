BiliExp-Actions
====  
##### 本分支为主分支的云函数功能的一部分，去除了对云函数的依赖，只需要github Actions就能使用

[![](https://img.shields.io/badge/author-%E6%98%9F%E8%BE%B0-red "作者")](https://github.com/happy888888/ )
![](https://img.shields.io/badge/dynamic/json?label=GitHub%20Followers&query=%24.data.totalSubs&url=https%3A%2F%2Fapi.spencerwoo.com%2Fsubstats%2F%3Fsource%3Dgithub%26queryKey%3Dhappy888888&labelColor=282c34&color=181717&logo=github&longCache=true "关注数量")
![](https://img.shields.io/github/stars/happy888888/BiliExp.svg?style=plastic&logo=appveyor "Star数量")
![](https://img.shields.io/github/forks/happy888888/BiliExp.svg?style=plastic&logo=stackshare "Fork数量")

### 主要功能
**B站自动操作脚本**
* [x] 自动获取经验(投币、点赞、分享视频) 
* [x] 自动转发互动抽奖
* [x] 参与官方抽奖活动(activity)
* [x] 直播辅助(直播签到，~~直播挂机~~，直播自动送出快过期礼物) 
* [x] 自动兑换银瓜子为硬币 
* [x] 自动领取大会员每月权益(B币劵，优惠券) 
* [x] 漫画辅助脚本(漫画APP签到，自动花费即将过期漫读劵，自动积分兑换漫画福利券) 
* [x] 定时清理无效动态(转发的过期抽奖，失效动态) 
* [ ] 直播开启宝箱领取银瓜子(本活动已结束，不知道B站以后会不会再启动) 
</br>

### 使用方式
* 1.准备
    *  1.1一个或多个B站账号，以及登录后获取的SESSDATA，bili_jct，DedeUserID (获取方式见最下方示意图)
    *  1.2SCKEY (可选，用于账号失效时用微信提醒,不用请留空，详情见http://sc.ftqq.com/)
    *  1.3fork本项目
* 2.部署
    *  2.1在fork后的github仓库的 “Settings” --》“Secrets” 中添加"Secrets"，name和value分别为：
        *  2.1.1 name为"biliconfig"           value为B站账号登录信息，格式参照config/config.json文件
    *  2.2添加完上面的"Secrets"后，进入"Actions" --》"run BiliExp"，点击右边的"Run workflow"即可第一次启动
        *  2.2.1 首次fork可能要去actions里面同意使用actions条款，如果"Actions"里面没有"run BiliExp"，点一下右上角的"star"，"run BiliExp"就会出现在"Actions"里面
        *  2.2.2 第一次启动后，脚本会每天12:00自动执行，不需要再次手动执行(第一次手动执行这个步骤不能忽略)。
```
    注:不要在github上直接在config/config.json中填写账号信息，而是在Secrets中填写，避免账号信息泄露。
```

### 2020/09/24更新

* 1.移除参加B站活动抽奖的脚本的活动列表文件，改为自动获取。(现在这个活动抽奖很鸡肋)

</br></br>


B站操作需要的cookie数据可以按照以下方式获取
浏览器打开B站主页--》按F12打开开发者工具--》application--》cookies
<div align="center"><img src="https://s1.ax1x.com/2020/09/23/wjM09e.png" width="800" height="450" title="获取cookies示例"></div>
