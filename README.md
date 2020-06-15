# nikki_auto_party

闪耀暖暖python脚本自动定时参加联盟答题（入夜派对）。
注：该脚本挂机成功率贼高（最近好像除了我忘记点开始以外没失败过），但是，每次换看板请替换下截图，以及，没有GUI，问就是没空写。

## 使用前配置
1. 下载模拟器，下载python并安装import语句里对应的包，并下载安装好闪暖。
2. 将auto_party.py第40行get_window_position()函数内的窗口名字改成你的模拟器窗口名字。
3. 将auto_party.py里所有的click_pos变量修改成你模拟器内对应的坐标。获取坐标可使用save_screenshots(get_window_position(), None, '图片名.png')截图模拟器窗口或任意工具按照screenshots文件夹里的示例截图，然后用Windows自带的画图打开截图->把鼠标挪到需要点击的位置->坐标在左下角
4. 将screenshots里名字为 `nikki_*.png` 对应的截图替换成你自己的，不换也许也可以，但是不能保证。**尤其是每次更新看板后请更新nikki_home.png**。
5. 可以uncomment掉倒数第二行的DEBUG_MODE = True执行调试下。

## 使用方法
1. 启动你的模拟器，如需多开，请同步多开窗口的操作。本脚本只会在其中一个模拟器上操作（即你在使用前配置步骤2里填写名字的窗口）。如果是好几个号，只有模拟器直接操作的那个窗口对应的号换看板了才需要更新看板截图。
2. 执行auto_party.py。执行方法：命令行里执行`python auto_party.py`或IDE内直接run。
