class Clipboard:
    @staticmethod
    def GetText():
        """
        获取剪贴板文本

        Clipboard.GetText()

        :return:剪切板的文本内容
        """
    @staticmethod
    def SetText(content: str = ''):
        '''
        设置剪贴板文本

        Clipboard.SetText(\'\')

        :param content:[必选参数]新的剪贴板文本内容，默认""
        :return:成功返回True，失败返回False
        '''
    @staticmethod
    def SetImage(picPath):
        """
        把图片放入剪贴板

        Clipboard.SetText(picPath)

        :param picPath:[必选参数]图片的路径
        :return:成功返回True，失败返回False
        """
    @staticmethod
    def SaveImage(savePath: str):
        """
        将剪贴板中的图片保存到文件

        Clipboard.SaveImage(savePath)

        :param savePath:[必选参数]需要保存的文件路径
        :return:保存成功返回True，保存失败返回False
        """
    @staticmethod
    def SetFile(paths: str | list):
        """
        把文件放入剪贴板

        Clipboard.SetFile(filePath)

        :param paths:[必选参数]文件的路径，单个文件用字符串，多个文件用list类型，其中每个元素用字符串
        :return:成功返回True，失败返回False
        """
