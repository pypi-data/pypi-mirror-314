from _typeshed import Incomplete
from playwright.sync_api import ElementHandle, Page as Page

class Web:
    @staticmethod
    def Exists(tdstr: str, anchorsElement, isVisible: bool = True) -> bool:
        """
        元素是否存在（不可见归于不存在）

        Web.Exists(tdstr, page, isVisible=True)

        :param tdstr: td字符串
        :param anchorsElement: 锚点参数
        :param isVisible:[可选参数]检查是否可见。默认True
        :return: bool
        """
    @staticmethod
    def Wait(tdstr: str, anchorsElement, waitType: str = 'show', searchDelay: int = 10000, continueOnError: bool = False, isVisible: bool = True) -> None:
        '''
        等待元素加载

        Web.Wait(tdstr, page, waitType=\'show\', searchDelay=10000, continueOnError=False, isVisible=True)

        :param tdstr: td字符串
        :param anchorsElement: 锚点元素
        :param waitType: [可选参数]等待方式。 等待显示："show" 等待消失:"hide"。默认"show"
        :param searchDelay:[可选参数]等待最大时间。默认10000毫秒（10秒）
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param isVisible:[可选参数]检查是否可见。默认True
        :return: None
        '''
    @staticmethod
    def GetParentElement(eh: ElementHandle) -> ElementHandle:
        """
        获取父级元素

        eh = Web.GetParentElement(eh)

        :param eh: ElementHandle
        :return: ElementHandle
        """
    @staticmethod
    def GetNextSiblingElement(eh: ElementHandle) -> ElementHandle:
        """
        获取下一个兄弟元素

        eh = Web.GetNextSiblingElement(eh)

        :param eh: ElementHandle
        :return: ElementHandle
        """
    @staticmethod
    def GetPreviousSiblingElement(eh: ElementHandle) -> ElementHandle:
        """
        获取前一个兄弟元素

        eh = Web.GetPreviousSiblingElement(eh)

        :param eh: ElementHandle
        :return: ElementHandle
        """
    @staticmethod
    def GetChildrenElements(eh) -> list:
        """
        获取子节点

        ehList = Web.GetChildrenElements(eh)

        :param eh: ElementHandle
        :return: list[ElementHandle, ElementHandle, ...]
        """
    @staticmethod
    def Click(target: str | ElementHandle, anchorsElement: Incomplete | None = None, position: Incomplete | None = None, delayTime: int = 10000) -> ElementHandle:
        """
        点击元素

        eh = Web.Click(target, page, position=None, delayTime=10000)

        :param target: tdstr 或 ElementHandle
        :param anchorsElement: 锚点元素
        :param position: 以元素左上角偏移量{'x': 0, 'y': 0}，None时点击中心
        :param delayTime: 超时（豪秒）。默认10000
        :return: ElementHandle
        """
    @staticmethod
    def Hover(target: str | ElementHandle, anchorsElement: Incomplete | None = None, position: Incomplete | None = None, delayTime: int = 10000) -> ElementHandle:
        """
        鼠标悬停在元素上

        eh = Web.Hover(target, page, position=None, delayTime=10000)

        :param target: tdstr 或 ElementHandle
        :param anchorsElement: 锚点元素
        :param position: 以元素左上角偏移量{'x': 0, 'y': 0}，None时点击中心
        :param delayTime: 超时（豪秒）。默认10000
        :return: ElementHandle
        """
    @staticmethod
    def Input(text, target, anchorsElement: Incomplete | None = None, delayTime: int = 10000) -> ElementHandle:
        """
        输入文本

        eh = Web.Input(text, target, page, delayTime=10000)

        :param text: 文本内容
        :param target: tdstr 或 ElementHandle
        :param anchorsElement: 锚点元素
        :param delayTime: 超时（豪秒）。默认10000
        :return: ElementHandle
        """
    @staticmethod
    def ClickLinkOpenNewPage(eh, position: Incomplete | None = None, waitLoad: bool = False) -> Page:
        """
        点击连接产生新的标签页

        newPage = Web.ClickLinkOpenNewPage(eh, position=None, waitLoad=False)

        :param eh: ElementHandle
        :param position: 以元素左上角偏移量{'x': 0, 'y': 0}，None时点击中心
        :param waitLoad: 是否等待新页面加载完毕。默认False
        :return: newPage
        """
    @staticmethod
    def FindWebElement(tdstr: str, anchorsElement, searchDelay: int = 10000, continueOnError: bool = False, isVisible: bool = True) -> ElementHandle:
        """
        查找元素

        eh = Web.FindWebElement(tdstr, page, searchDelay=10000, continueOnError=False, isVisible=True)

        :param tdstr: td字符串
        :param anchorsElement: 锚点参数
        :param searchDelay: 查找延时（豪秒）。默认10000
        :param continueOnError: 错误继续执行。默认False
        :param isVisible:检查是否可见。默认True
        :return: ElementHandle
        """
    @staticmethod
    def PwStart(port: int = 9222, magic: bool = True) -> Page:
        """
        绑定浏览器

        page = Web.PwStart()

        :return:  firstPage
        """
    @staticmethod
    def OpenChrome(url: str = None, chromeExePath: str = None, isMaximize: bool = True, supportUia: bool = True, userData: Incomplete | None = None, otherStartupParam: Incomplete | None = None, env_variables: Incomplete | None = None, delayTime: int = 30000) -> None:
        '''
        启动谷歌浏览器

        Web.OpenChrome(url="www.baidu.com", chromeExePath=None, isMaximize=True, supportUia=True, userData=None, otherStartupParam=None, env_variables=None, delayTime=30000)

        :param url:[可选参数]启动浏览器后打开的链接，字符串类型。默认None
        :param chromeExePath:[可选参数]谷歌浏览器可执行程序的绝对路径，字符串类型，填写None时会自动寻找本地安装的路径。默认None
        :param isMaximize:[可选参数]浏览器启动后是否最大化显示，选择True时最大化启动，选择False默认状态。默认True
        :param supportUia:[可选参数]是否支持uiautomatin，True支持，False不支持。默认True
        :param userData:[可选参数]浏览器用户数据存放位置
        :param otherStartupParam:[可选参数]其他启动谷歌浏览器的参数，如：[\'--xxx\', \'--xxx\']。默认None
        :param env_variables:[可选参数]启动浏览器进程时附带的环境变量，如{"a": "abc"}
        :param delayTime: 浏览器进程加载超时(毫秒)。默认30000
        :return:None
        '''
    @staticmethod
    def ChromeProcessStatus() -> bool:
        """
        检查启动的Chrome浏览器进程是否正在运行

        chromeStatus = Web.ChromeProcessStatus()

        :return:返回True时，表示浏览器仍在运行，返回False时，表示浏览器非运行状态
        """
    @staticmethod
    def TopMost() -> None:
        """
        浏览器置顶

        Web.TopMost()

        """

class ChromePlugin:
    @staticmethod
    def Open(url: str = None, clearChrome: bool = True, userData: str = None, otherStartupParam: list = None):
        """
        启动新的浏览器

        ChromePlugin.Open(url='www.baidu.com', clearChrome=True, userData=None, otherStartupParam=None)

        """
    @staticmethod
    def JS(js_str: str, returnList: bool = False):
        """
        执行JS注入

        ChromePlugin.JS(js_str, returnList=False)

        """
    @staticmethod
    def Close(tryClose: int = 3, userData: str = None):
        """
        关闭chrome

        ChromePlugin.Close(tryClose=3, userData=None)

        """
    @staticmethod
    def WaitLoading(delayTime: int = 60000) -> None:
        """
        等待加载

        ChromePlugin.WaitLoading(delayTime=60000)

        """
    @staticmethod
    def Reload() -> None:
        """
        刷新页面

        ChromePlugin.Reload()

        """
    @staticmethod
    def GoUrl(url, isWaitLoading: bool = True, delayTime: int = 60000) -> None:
        """
        跳转页面

        ChromePlugin.GoUrl('www.baidu.com', isWaitLoading=True, delayTime=60000)

        """
