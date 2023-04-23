import sys
from enum import Enum
import xlrd
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class CaseElement(Enum):
    # 用例要素
    ID = '编号'
    STEP = '执行步骤'
    PLACE = '元素位置'
    WAY = '操作方式'
    PARAMETER = '参数'
    RESULT = '结果'
    # 数据键名
    SHEETS = 'sheets'
    SHEETKEY = 'sheet_key'
    CASE = 'cases'
    CASEKEY = 'case_key'
    STEPS = 'steps'
    STEPKEY = 'step_key'
    # 操作方式
    INPUT = 'input'
    CLICK = 'click'
    TEXT = 'text'
    SLEEP = 'sleep'
    URL = 'url'


class GetCases(object):
    """
    用例管理类
            提供处理用例文件的类方法：
            read_excel:读取用例文件
            processing：对read_excel读取的数据进行预处理
            get_step_data：获取用例步骤中各要素的参数集合
    """
    driver = None  # 获取浏览器对象
    sheet_names = []
    sheet_names_map = {}
    allMessage = ''

    @classmethod
    def read_excel(cls, file_name, assign_sheet=None):
        """
        读取用例文件（excel）
        :param file_name: 必传(str)：传入需要读取的excel文件路径
        :param assign_sheet: 非必传(str)，传参数时读取整个excel文件
                            传入需要读取的指定画布名称，则读取单
                            画布内的用例数据。
        :return: 未传assign_sheet时，返回整个excel全部用例数据。
                传入assign_sheet时，返回指定画布下的用例数据
        """
        try:
            book = xlrd.open_workbook(file_name)
            if book.sheet_names() is None:
                return False

            for i in range(len(book.sheet_names())):
                if assign_sheet is not None:
                    sheet_name = assign_sheet
                else:
                    sheet_name = book.sheet_names()[i]
                if "DEL" in sheet_name:
                    continue
                cls.sheet_names.append(sheet_name)
                case_list = cls.parse_map(book, sheet_name)
                cls.sheet_names_map[sheet_name] = case_list
                if assign_sheet is not None:
                    break

        except Exception as e:
            print('配置.xls不存在，请根据 配置模板.xls 模板创建 配置.xls 文件')

            sys.exit(1)

    @classmethod
    def parse_map(cls, book, sheet_name):
        sheet = book.sheet_by_name(sheet_name)
        case_list = []
        for line in range(sheet.nrows):  # 遍历行
            if line == 0:
                continue
            dataset = {}
            if (sheet.cell(line, 0).value > -1):
                dataset['index'] = sheet.cell(line, 0).value
                dataset['step'] = sheet.cell(line, 1).value
                dataset['location'] = sheet.cell(line, 2).value
                dataset['way'] = sheet.cell(line, 3).value
                dataset['param'] = sheet.cell(line, 4).value
                dataset['result'] = sheet.cell(line, 5).value
                case_list.append(dataset)
        return case_list

    @classmethod
    def processing(cls):
        """
        对excel读取出来的数据进行分解，简化数据处理过程
        """
        for i in range(len(GetCases.sheet_names)):
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            sheet_name = GetCases.sheet_names[i]
            dataset = GetCases.sheet_names_map[sheet_name]
            website = "【" + sheet_name + "】"
            for y in range(len(dataset)):
                cell = dataset[y]
                try:
                    if cell['location'] != '':
                        # operate = GetCases.driver.find_element(By.XPATH, cell['location'])  # 定位元素（写死XPATH）--牺牲定位效率，简化用例编写
                        wait = WebDriverWait(GetCases.driver, 5)
                        operate = wait.until(ec.element_to_be_clickable((By.XPATH, cell['location'])))
                        if cell['way'] == CaseElement.INPUT.value:  # 键入
                            operate.send_keys(cell['param'])
                        elif cell['way'] == CaseElement.CLICK.value:  # 点击
                            print(website, '点击', cell['step'])
                            operate.click()
                        elif cell['way'] == CaseElement.TEXT.value:  # 获取文本
                            print(website, cell['step'], operate.text)
                            GetCases.allMessage = f'{GetCases.allMessage}{website} {cell["step"]} {operate.text}\n'
                    elif cell['way'] == CaseElement.SLEEP.value:  # 显式等待
                        print(website, '等待 %d 秒~~~' % cell['param'])
                        sleep(cell['param'])
                    elif cell['way'] == CaseElement.URL.value:  # 打开链接
                        print(website, '打开链接', cell['param'])
                        DriverUtil.get_driver().get(cell['param'])
                    else:
                        raise Exception(website, '元素位置为空哦，检查一下吧~')
                except Exception as e:
                    print(website, cell['step'], '操作失败')
                finally:
                    if cell['param'] == "break":
                        break
                    else:
                        continue


class DriverUtil(object):
    """浏览器对象管理类"""
    __driver = None

    @classmethod
    def get_driver(cls, website=None):
        """"获取浏览器对象方法"""
        if cls.__driver is None:
            # 创建chrome对象
            opt = webdriver.ChromeOptions()
            # 解决DevToolsActivePort 文件不存在的报错
            # opt.add_argument('--no-sandbox')
            # 指定浏览器分辨率
            # opt.add_argument('window-size=1600x900')
            # 规避Bug
            # opt.add_argument('--disable-gpu')
            # 隐藏滚动条
            # opt.add_argument('--hide-scrollbars')
            # 不加载图片,提速
            # opt.add_argument('blink-settings=imagesEnabled=false')
            # 不提供可视化
            # opt.add_argument('--headless')

            cls.__driver = webdriver.Chrome(chrome_options=opt)  # 运行会自动打开谷歌浏览器,上面会有提示,Chrome正受到自动化测试工具的控制
            # 将浏览器窗口最大化
            cls.__driver.maximize_window()
            # cls.__driver.get(website)
            # cls.__driver.maximize_window()
            cls.__driver.implicitly_wait(5)
        return cls.__driver

    @classmethod
    def quit_driver(cls):
        """"退出浏览器对象方法"""
        # sleep(2)
        cls.__driver.quit()
        cls.__driver = None
