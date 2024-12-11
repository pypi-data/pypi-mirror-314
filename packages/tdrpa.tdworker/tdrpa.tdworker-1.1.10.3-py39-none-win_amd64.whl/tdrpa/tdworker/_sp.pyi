class PrintToScreen:
    @staticmethod
    def DrawText(msg: str = '', showSec: int = 0) -> None:
        '''
        绘制屏幕中央正上方显示的红字

        PrintToScreen.DrawText(\'开始工作\', showSec=0)

        :param msg:[可选参数]文字内容，默认为""
        :param showSec:[可选参数]显示秒数。0:一直显示到程序结束，大于0:显示的时间，单位是秒
        :return:无
        '''
    @staticmethod
    def CleanText() -> None:
        """
        清除屏幕中央正上方显示的红字

        PrintToScreen.CleanText()

        :return:无
        """