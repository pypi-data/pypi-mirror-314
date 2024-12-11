import uiautomation as uia

class Window:
    @staticmethod
    def Close(target: str | uia.Control) -> None:
        """
        关闭窗口

        Window.Close(target)

        :param target: [必选参数]tdRPA拾取器获取的目标窗口元素特征字符串或uia目标窗口元素对象，也可选取窗口内始终存在的元素。
        :return: None
        """
    @staticmethod
    def GetActive(isReturnHwnd: bool = True) -> uia.Control | int:
        """
        获取活动窗口

        Window.GetActive(isReturnHwnd=True)

        :param isReturnHwnd: [可选参数]是否返回窗口句柄，True时函数返回窗口句柄，False时返回窗口元素对象。默认True
        :return:窗口句柄或者窗口元素对象
        """
    @staticmethod
    def SetActive(target: str | uia.Control) -> bool:
        """
        设置活动窗口

        Window.SetActive(target)

        :param target: [必选参数]tdRPA拾取器获取的目标窗口元素特征字符串或uia目标窗口元素对象，也可选取窗口内始终存在的元素。
        :return: bool。激活成功返回True，否则返回False
        """
    @staticmethod
    def Show(target: str | uia.Control, showStatus: str = 'show') -> bool:
        '''
        更改窗口显示状态

        Window.Show(target, showStatus="show")

        :param target: [必选参数]tdRPA拾取器获取的目标窗口元素特征字符串或uia目标窗口元素对象，也可选取窗口内始终存在的元素。
        :param showStatus: [可选参数] 显示：\'show\' 隐藏：\'hide\' 最大化：\'max\' 最小化：\'min\' 还原：\'restore\'。默认\'show\'
        :return: bool。执行成功返回True，否则返回False
        '''
    @staticmethod
    def Exists(target: str | uia.WindowControl) -> bool:
        """
        判断窗口是否存在

        Window.Exists(target)

        :param target: [必选参数]tdRPA拾取器获取的目标窗口元素特征字符串或uia目标窗口元素对象
        :return: bool。窗口存在返回True,否则返回False
        """
    @staticmethod
    def GetSize(target: str | uia.Control) -> dict:
        '''
        获取窗口大小

        Window.GetSize(target)

        :param target: [必选参数]tdRPA拾取器获取的目标窗口元素特征字符串或uia目标窗口元素对象，也可选取窗口内始终存在的元素。
        :return: {"height":int, "width":int, "x":int, "y":int}
        '''
    @staticmethod
    def SetSize(target: str | uia.Control, width: int, height: int) -> None:
        """
        改变窗口大小

        Window.SetSize(target, 800, 600)

        :param target: [必选参数]tdRPA拾取器获取的目标窗口元素特征字符串或uia目标窗口元素对象，也可选取窗口内始终存在的元素。
        :param width: [必选参数]窗口宽度
        :param height: [必选参数]窗口高度
        :return: None
        """
    @staticmethod
    def Move(target: str | uia.Control, x: int, y: int) -> None:
        """
        移动窗口位置

        Window.Move(target, 0, 0)

        :param target: [必选参数]tdRPA拾取器获取的目标窗口元素特征字符串或uia目标窗口元素对象，也可选取窗口内始终存在的元素。
        :param x: [必选参数]移动到新位置的横坐标
        :param y: [必选参数]移动到新位置的纵坐标
        :return: None
        """
    @staticmethod
    def TopMost(target: str | uia.Control, isTopMost: bool = True) -> bool:
        """
        窗口置顶

        Window.TopMost(target, isTopMost=True)

        :param target: [必选参数]tdRPA拾取器获取的目标窗口元素特征字符串或uia目标窗口元素对象，也可选取窗口内始终存在的元素。
        :param isTopMost: [可选参数]是否使窗口置顶，窗口置顶:true 窗口取消置顶:false。默认True
        :return: bool值，设置成功返回True，否则返回False
        """
    @staticmethod
    def GetClass(target: str | uia.Control) -> str:
        """
        获取窗口类名

        Window.GetClass(target)

        :param target: [必选参数]tdRPA拾取器获取的目标窗口元素特征字符串或uia目标窗口元素对象，也可选取窗口内始终存在的元素。
        :return: 窗口的类名称
        """
    @staticmethod
    def GetPath(target: str | uia.Control) -> str:
        """
        获取窗口程序的文件路径

        Window.GetPath(target)

        :param target: [必选参数]tdRPA拾取器获取的目标窗口元素特征字符串或uia目标窗口元素对象，也可选取窗口内始终存在的元素。
        :return: 文件绝对路径
        """
    @staticmethod
    def GetPID(target: str | uia.Control) -> int:
        """
        获取进程PID

        Window.GetPID(target)

        :param target: [必选参数]tdRPA拾取器获取的目标窗口元素特征字符串或uia目标窗口元素对象，也可选取窗口内始终存在的元素。
        :return: PID
        """
