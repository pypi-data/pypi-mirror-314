import uiautomation as uia

class WinKeyboard:
    @staticmethod
    def InputText(target: str | uia.Control, content: str, clearOldText: bool = True, inputInterval: int = 10, searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100, setForeground: bool = True, simulateType: str = 'message', validate: bool = False, clickBeforeInput: bool = False) -> uia.Control:
        '''
        在目标中输入

        WinKeyboard.InputText(target, \'\', clearOldText=True, inputInterval=10, searchDelay=10000, anchorsElement=None, continueOnError=False, delayAfter=100, delayBefore=100, setForeground=True, simulateType=\'message\', validate=False, clickBeforeInput=False)

        :param target: [必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param content: [必选参数]写入文本
        :param clearOldText: [可选参数]是否清空原内容。默认True
        :param inputInterval: [可选参数]键入间隔(毫秒)。默认10
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :param setForeground: [可选参数]激活窗口。默认True
        :param simulateType: [可选参数]操作类型。模拟操作:"simulate" 消息操作:"message"。默认"message"
        :param validate: [可选参数]验证写入文本。默认False
        :param clickBeforeInput: [可选参数]输入前点击。默认False
        :return: 目标元素对象
        '''
    @staticmethod
    def PressKey(target: str | uia.Control, button: str, searchDelay: int = 10000, anchorsElement: uia.Control = None, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100, setForeground: bool = True, keyModifiers: list = None, simulateType: str = 'message', clickBeforeInput: bool = False) -> uia.Control:
        '''
        在目标中按键

        WinKeyboard.PressKey(target, "Enter", searchDelay=10000, continueOnError=False, delayAfter=100, delayBefore=100, setForeground=True, keyModifiers=None, simulateType=\'message\', clickBeforeInput=False)

        :param target: [必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param button: [必选参数]键盘按键上的符号。如"Enter"
        :param searchDelay: [可选参数]超时时间(毫秒)。默认10000
        :param anchorsElement: [可选参数]锚点元素，从它开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param continueOnError: [可选参数]错误继续执行。默认False
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :param setForeground: [可选参数]激活窗口。默认True
        :param keyModifiers: [可选参数]辅助按键[\'Alt\',\'Ctrl\',\'Shift\',\'Win\']可多选。默认None
        :param simulateType: [可选参数]操作类型。模拟操作:"simulate" 消息操作:"message"。默认"message"
        :param clickBeforeInput: [可选参数]输入前点击。默认False
        :return: 目标元素对象
        '''
    @staticmethod
    def Input(content: str, inputInterval: int = 10, delayAfter: int = 100, delayBefore: int = 100, simulateType: str = 'message') -> None:
        '''
        输入文本

        WinKeyboard.Input(\'\', inputInterval=10, delayAfter=100, delayBefore=100, simulateType=\'message\')

        :param content: [必选参数]输入内容
        :param inputInterval: [可选参数]键入间隔(毫秒)。默认10
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :param simulateType: [可选参数]操作类型。模拟操作:"simulate" 消息操作:"message"。默认"message"
        :return: None
        '''
    @staticmethod
    def Press(button: str, pressType: str = 'press', keyModifiers: list = None, delayAfter: int = 100, delayBefore: int = 100, simulateType: str = 'message') -> None:
        '''
        模拟按键

        WinKeyboard.Press(\'Enter\', pressType=\'press\', keyModifiers=None, delayAfter=100, delayBefore=100, simulateType=\'message\')

        :param button: [必选参数]键盘按键上的符号，如“Enter”
        :param pressType: [可选参数]点击类型。单击:"press" 按下:"down" 弹起:"up"。默认"press"
        :param keyModifiers: [可选参数]辅助按键["Alt","Ctrl","Shift","Win"]可多选。默认None
        :param delayAfter: [可选参数]执行后延时(毫秒)。默认100
        :param delayBefore: [可选参数]执行前延时(毫秒)。默认100
        :param simulateType: [可选参数]操作类型。模拟操作:"simulate" 消息操作:"message"。默认"message"
        :return: None
        '''
