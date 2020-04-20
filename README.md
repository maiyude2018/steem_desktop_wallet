# steem_desktop_warret
 功能基本和网页版一样，功能有：

- 1.转账（steem，sbd，hive，hbd以及scot都可以转）
- 2.power up & down
- 3.代理SP操作
- 4.scot一键清理以及steemp提现
- 5.创建新账号
- 6.见证人投票



/requirements/base.txt  #这是需要安装的依赖包

/SUI  #UI美化包

/acc.db #账号数据库文件

/main.py #主程序

/steemwaller.py #UI程序

/steemwaller.ui #pyqt5_UI文件

/steems_top.rar  #打包好的win7  EXE程序，打开即可使用


### 如果你要自己打包程序

1.首先安装/requirements/base.txt 里面的依赖包
```
pip install --upgrade -r requirements/base.txt
```

2.使用pyinstall打包程序，建议使用虚拟环境，文件会小一点.[参考文章](https://blog.csdn.net/laiyaoditude/article/details/85278037)
```
pyinstaller -F main.py
```

3.复制SUI文件夹和acc.db，和EXE文件放在同一目录。
