import uiautomation as uia

class WinElement:
    @staticmethod
    def FindElementByTd(tdTargetStr: str = None, anchorsElement: uia.Control = None, searchDelay: int = 10000, continueOnError: bool = False):
        """
        依据tdrpa拾取器获取的元素特征码查找元素

        WinElement.FindElementByTd('', anchorsElement=None, searchDelay=10000, continueOnError=False)

        :param tdTargetStr: 目标元素特征码(tdrpa拾取器获取)
        :param anchorsElement: 从哪个元素开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）
        :param searchDelay: 查找延时（豪秒）。默认10000
        :param continueOnError: 错误继续执行。默认False
        :return: 目标元素 or None
        """
    @staticmethod
    def GetChildren(target: str | uia.Control, searchType: str = 'all', searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> list | uia.Control:
        '''
        获取子元素

        WinElement.GetChildren(target, searchType=\'all\', searchDelay=10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param searchType: [可选参数]搜索方式。全部子元素:"all" 首个子元素:"first" 最后一个子元素:"last"。默认"all"
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: 目标元素对象的子元素列表 或 首个子元素 或 最后一个子元素
        '''
    @staticmethod
    def GetParent(target: str | uia.Control, upLevels: int = 1, searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> uia.Control:
        """
        获取父元素

        WinElement.GetParent(target, upLevels=1, searchDelay=10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param upLevels: [可选参数]父元素层级，1为父元素，2为祖父元素，3为曾祖父元素，以此类推，0为当前元素的顶层窗口元素。默认1
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: 目标元素对象的上一层父级元素 或 顶层父级元素
        """
    @staticmethod
    def GetSibling(target: str | uia.Control, position: str = 'next', searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> uia.Control | None:
        '''
        获取相邻元素

        WinElement.GetSibling(target, position="next", searchDelay=10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param position: [可选参数]相邻位置。下一个："next"  上一个："previous"。默认"next"
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: 目标元素对象的下一个相邻元素对象 或 上一个相邻元素对象，没有返回None
        '''
    @staticmethod
    def Exists(target: str | uia.Control, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> bool:
        """
        判断元素是否存在

        WinElement.Exists(target, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: bool
        """
    @staticmethod
    def GetCheck(target: str | uia.Control, searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> bool:
        """
        获取元素勾选

        WinElement.GetCheck(target, searchDelay=10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: bool
        """
    @staticmethod
    def SetCheck(target: str | uia.Control, isCheck: bool = True, searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> bool:
        """
        设置元素勾选

        WinElement.SetCheck(target, isCheck=True, searchDelay=10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param isCheck: [可选参数]设置勾选:True 设置取消勾选:False。默认True
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: 执行成功返回True，执行失败返回False
        """
    @staticmethod
    def GetSelect(target: str | uia.Control, mode: str = 'text', searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> str | int:
        '''
        获取元素选择

        WinElement.GetSelect(target, mode=\'text\', searchDelay=10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param mode: [可选参数]获取文本："text" 获取序号：“index” 获取值：“value”。默认"text"
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: 已选项的文本 或 序号 或 值，没有则返回None
        '''
    @staticmethod
    def SetSelect(target: str | uia.Control, option: str | int, mode: str = 'text', searchDelay: int = 10000, anchorsElement: uia.Control = None, setForeground: bool = True, cursorPosition: str = 'center', cursorOffsetX: int = 0, cursorOffsetY: int = 0, simulateType: str = 'simulate', continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> None:
        '''
        设置元素选择

        WinElement.SetSelect(target, \'\', mode="text", searchDelay=10000, anchorsElement=None, setForeground=True, cursorPosition=\'center\', cursorOffsetX=0, cursorOffsetY=0, simulateType=\'simulate\', continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param option: [必选参数]选择选项的文本或者序号
        :param mode: [可选参数]选择文本："text" 选择序号：“index” 选择值：“value”。默认"text"
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param setForeground: [可选参数]激活窗口。默认True
        :param cursorPosition: [可选参数]光标在选中项的位置。中心:"center" 左上角:"topLeft" 右上角:"topRight" 左下角:"bottomLeft" 右下角:"bottomRight"。默认"center"
        :param cursorOffsetX: [可选参数]横坐标偏移。默认0
        :param cursorOffsetY: [可选参数]纵坐标偏移。默认0
        :param simulateType: [可选参数]鼠标点击选中项时的模式。模拟操作:"simulate" 消息操作:"message"。默认"simulate"
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: None
        '''
    @staticmethod
    def GetValue(target: str | uia.Control, getMethod: str = 'auto', searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> str:
        '''
        获取元素文本

        WinElement.GetValue(target, getMethod="auto", searchDelay=10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param getMethod: [可选参数]获取方式。自动方式："auto" 获得元素Name方式："name" 获得元素Value方式："value"。默认"auto"
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: 元素文本
        '''
    @staticmethod
    def SetValue(target: str | uia.Control, value: str, searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> None:
        '''
        设置元素文本

        WinElement.SetValue(target, "", searchDelay=10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param value: [必选参数]要写入元素的文本内容
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: None
        '''
    @staticmethod
    def GetRect(target: str | uia.Control, relativeType: str = 'parent', searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> dict:
        '''
        获取元素区域

        WinElement.GetRect(target, relativeType="parent", searchDelay=10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param relativeType: [可选参数]返回元素位置是相对于哪一个坐标而言的。 相对父元素:"parent" 相对窗口客户区:"root" 相对屏幕坐标:"screen"。默认"parent"
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: {"height" : int, "width" : int, "x" : int, "y" : int}
        '''
    @staticmethod
    def ScreenCapture(target: str | uia.Control, filePath: str, rect: dict = None, searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> bool:
        '''
        元素截图

        WinElement.ScreenCapture(target, \'D:/1.png\', rect=None, searchDelay=10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param filePath: [必选参数]图片存储的绝对路径。如 \'D:/1.png\'(支持图片保存格式：bmp、jpg、jpeg、png、gif、tif、tiff)
        :param rect: [可选参数]对指定界面元素截图的范围，若传None，则截取该元素的全区域。若传{"x":int,"y":int,"width":int,"height":int}，则以该元素左上角位置偏移x,y的坐标为原点，根据高宽进行截图。默认None
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: bool(截图成功返回True，否则返回假)
        '''
    @staticmethod
    def Wait(target: str | uia.Control, waitType: str = 'show', searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> None:
        '''
        等待元素（等待元素显示或消失）

        WinElement.Wait(target, waitType=\'show\', searchDelay=10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100)

        :param target: [必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param waitType: [可选参数]等待方式。 等待显示："show" 等待消失:"hide"。默认"show"
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: None
        '''

# class WinText:
#     @staticmethod
#     def GetText(target: str | uia.Control, searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100, setForeground: bool = True):
#         """
#         获取文本内容

#         WinText.GetText(target, searchDelay=10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100, setForeground=True)

#         :param target: [必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
#         :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
#         :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
#         :param continueOnError: [可选参数]错误继续执行。默认False
#         :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
#         :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
#         :param setForeground: [可选参数]激活窗口。默认True
#         :return: 文本内容
#         """
