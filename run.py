#!/usr/bin/env python3

import utils
from utils import DriverUtil
from notify import Notify
import config
import sys

if len(sys.argv) > 1:
    xls_path = sys.argv[1]
else:
    xls_path = f'{config.get_root()}/配置.xls'

print(f'读取配置文件位置：{xls_path}')
if __name__ == '__main__':
    # webdriver.Chrome()
    # 0.获取配置对象
    utils.GetCases.read_excel(xls_path)
    # 1.创建对象. 大写的C
    utils.GetCases.driver = DriverUtil.get_driver()
    # 手动指定浏览器驱动
    # chrome_obj = Chrome(executable_path='驱动文件的绝对路径/chromedriver.exe')  # 运行会自动打开谷歌浏览器,上面会有提示,Chrome正受到自动化测试工具的控制
    # 2.执行任务
    try:
        utils.GetCases.processing()
        print()
        print()
        print(utils.GetCases.allMessage)
        if config.conf().get("IS_SEND_NOTIFY"):
            Notify.sendQywx("获取成功", utils.GetCases.allMessage)
    finally:
        # 3.关闭浏览器
        DriverUtil.quit_driver()
        pass
