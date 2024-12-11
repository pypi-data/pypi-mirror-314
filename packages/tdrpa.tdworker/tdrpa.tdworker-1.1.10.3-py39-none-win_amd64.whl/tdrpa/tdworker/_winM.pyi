import uiautomation as uia

class WinMouse:
    @staticmethod
    def Action(target: str | uia.Control, button: str = 'left', clickType: str = 'click', searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100, setForeground: bool = True, cursorPosition: str = 'center', cursorOffsetX: int = 0, cursorOffsetY: int = 0, keyModifiers: list = None, simulateType: str = 'simulate', moveSmoothly: bool = False) -> uia.Control:
        '''
        点击目标元素

        WinMouse.Action(target, button="left", clickType="click", searchDelay=10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100, setForeground=True, cursorPosition=\'center\', cursorOffsetX=0, cursorOffsetY=0, keyModifiers=None, simulateType=\'simulate\', moveSmoothly=False)

        :param target: [必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param button: [可选参数]鼠标点击。鼠标左键:"left" 鼠标右键:"right" 鼠标中键:"middle"。默认"left"
        :param clickType: [可选参数]点击类型。单击:"click" 双击:"dbclick" 按下:"down" 弹起:"up"。默认"click"
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :param setForeground: [可选参数]激活窗口。默认True
        :param cursorPosition: [可选参数]光标位置。中心:"center" 左上角:"topLeft" 右上角:"topRight" 左下角:"bottomLeft" 右下角:"bottomRight"。默认"center"
        :param cursorOffsetX: [可选参数]横坐标偏移。默认0
        :param cursorOffsetY: [可选参数]纵坐标偏移。默认0
        :param keyModifiers: [可选参数]辅助按键["Alt","Ctrl","Shift","Win"]可多选。默认None
        :param simulateType: [可选参数]操作类型。模拟操作:"simulate" 消息操作:"message"。默认"simulate"
        :param moveSmoothly: [可选参数]是否平滑移动鼠标。默认False
        :return:目标元素对象
        '''
    @staticmethod
    def Hover(target: str | uia.Control, searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100, setForeground: bool = True, cursorPosition: str = 'center', cursorOffsetX: int = 0, cursorOffsetY: int = 0, keyModifiers: list = None, simulateType: str = 'simulate', moveSmoothly: bool = True) -> uia.Control:
        '''
        移动到目标上

        WinMouse.Hover(target, searchDelay=10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100, setForeground=True, cursorPosition=\'center\', cursorOffsetX=0, cursorOffsetY=0, keyModifiers=None, simulateType=\'simulate\', moveSmoothly=False)

        :param target: [必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :param setForeground: [可选参数]激活窗口。默认True
        :param cursorPosition: [可选参数]光标位置。中心:"center" 左上角:"topLeft" 右上角:"topRight" 左下角:"bottomLeft" 右下角:"bottomRight"。默认"center"
        :param cursorOffsetX: [可选参数]横坐标偏移。默认0
        :param cursorOffsetY: [可选参数]纵坐标偏移。默认0
        :param keyModifiers: [可选参数]辅助按键["Alt","Ctrl","Shift","Win"]可多选。默认None
        :param simulateType: [可选参数]操作类型。模拟操作:"simulate" 消息操作:"message"。默认"simulate"
        :param moveSmoothly: [可选参数]平滑移动。默认True
        :return:目标元素对象
        '''
    @staticmethod
    def Click(button: str = 'left', clickType: str = 'click', keyModifiers: list = None, delayAfter: int = 100, delayBefore: int = 100) -> None:
        '''
        模拟点击

        WinMouse.Click(button="left", clickType="click", keyModifiers=None, delayAfter=100, delayBefore=100)

        :param button: [可选参数]鼠标点击。鼠标左键:"left" 鼠标右键:"right" 鼠标中键:"middle"。默认"left"
        :param clickType: [可选参数]点击类型。单击:"click" 双击:"dbclick" 按下:"down" 弹起:"up"。默认"click"
        :param keyModifiers: [可选参数]辅助按键["Alt","Ctrl","Shift","Win"]可多选。默认None
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: None
        '''
    @staticmethod
    def Move(x: int, y: int, isRelativeMove: bool = False, delayAfter: int = 100, delayBefore: int = 100) -> None:
        """
        # 模拟移动

        WinMouse.Move(0, 0, isRelativeMove=False, delayAfter=100, delayBefore=100)

        :param x: [必选参数]横坐标
        :param y: [必选参数]纵坐标
        :param isRelativeMove: [可选参数]是否相对目前位置移动。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: None
        """
    @staticmethod
    def GetPos() -> tuple[int, int]:
        """
        获取鼠标位置

        WinMouse.GetPos()

        :return:pointX, pointY
        """
    @staticmethod
    def Drag(x1: int, y1: int, x2: int, y2: int, button: str = 'left', keyModifiers: list = None, delayAfter: int = 100, delayBefore: int = 100) -> None:
        '''
        模拟拖动

        WinMouse.Drag(0, 0, 0, 0, button=\'left\', keyModifiers=None, delayAfter=100, delayBefore=100)

        :param x1: [必选参数]起始横坐标
        :param y1: [必选参数]起始纵坐标
        :param x2: [必选参数]结束横坐标
        :param y2: [必选参数]结束纵坐标
        :param button: [可选参数]鼠标按键。鼠标左键:"left" 鼠标右键:"right" 鼠标中键:"middle"。默认"left"
        :param keyModifiers: [可选参数]辅助按键["Alt","Ctrl","Shift","Win"]可多选。默认None
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: None
        '''
    @staticmethod
    def Wheel(scrollNum: int, scrollDirection: str = 'down', keyModifiers: list = None, delayAfter: int = 100, delayBefore: int = 100) -> None:
        '''
        模拟滚轮

        WinMouse.Wheel(1, scrollDirection="down", keyModifiers=None, delayAfter=100, delayBefore=100)

        :param scrollNum: [必选参数]滚动次数
        :param scrollDirection: [可选参数]滚动方向。向上:"up" 向下:"down"。默认"down"
        :param keyModifiers: [可选参数]辅助按键["Alt","Ctrl","Shift","Win"]可多选。默认None
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :return: None
        '''
