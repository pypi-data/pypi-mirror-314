class App:
    @staticmethod
    def Kill(processName: str | int) -> bool:
        """
        强制停止应用程序的运行（结束进程）

        App.Kill('chrome.exe')

        :param processName:[必选参数]应用程序进程名或进程PID，忽略大小写字母
        :return:命令执行成功返回True，失败返回False
        """
    @staticmethod
    def GetStatus(processName: str | int, status: int = 0) -> bool:
        """
        获取应用运行状态

        App.GetStatus('chrome.exe', status=0)

        :param processName:[必选参数]应用程序进程名或进程PID，忽略大小写字母
        :param status:[可选参数]筛选进程状态。0:所有状态 1:运行 2:暂停 3:未响应 4:未知。默认0
        :return:进程存在返回True，不存在返回False
        """
    @staticmethod
    def Run(exePath, waitType: int = 0, showType: int = 1, mode: int = 0):
        """
        启动应用程序

        App.Run('''C:\\Windows\\system32\\mspaint.exe''')

        :param exePath:[必选参数]应用程序文件路径
        :param waitType:[可选参数]0:等待 1：等待应用程序准备好 2：等待应用程序执行到退出。默认0
        :param showType:[可选参数]程序启动后的显示样式（不一定生效） 0：隐藏 1：默认 3：最大化 6：最小化
        :param mode:[可选参数]启动模式，0:常规模式启动, 1:增强模式启动。当常规模式启动后无法拾取元素时，可尝试增强模式启动。默认0
        :return:返回应用程序的PID
        """
    @staticmethod
    def WaitProcess(processName, waitType: str = 'open', delayTime: int = 30000) -> bool:
        '''
        等待应用启动或关闭

        App.WaitProcess(\'chrome.exe\', waitType=\'open\', delayTime=30000)

        :param processName:[必选参数]进程名称，忽略大小写字母。如:"chrome.exe"
        :param waitType:[可选参数]期望应用状态。open:等待应用打开 close:等待应用关闭
        :param delayTime:[可选参数]最大等待时间，默认30000毫秒(即30秒)
        :return:等待时间内达到期望应用状态（开启/关闭）返回True，否则返回False
        '''
