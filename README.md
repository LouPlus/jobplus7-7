# jobplus7-7
LouPlus Team 7 https://github.com/LouPlus/jobplus7-7

## Contributors
* [webxuejun](https://github.com/xue99999)
* [buyseven](https://github.com/buyseven)
* [lou_cal](https://github.com/tsunemori-akane)
* [naxiehuaer2008](https://github.com/naxiehuaer2008)
* [li李多多](https://github.com/66li)

## requirements 依赖包
强制以python3来安装依赖包
```python
sudo python3 -m pip install -r requirements.txt
```

## 添加测试数据
创建数据库jobplus


```python
flask db upgrade

flask shell

from scripts.generate_test_datas import run
run()
```

## 测试账户
密码统一为 123123
* 求职者 test@qq.com

* 企业 shiyanlou_1_@qq.com

* 管理员 admin@qq.com

## 补充说明
目前只有第一个企业有投递信息


