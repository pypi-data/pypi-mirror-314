from _typeshed import Incomplete
import uiautomation as uia

SCT: Incomplete

class Image:
    @staticmethod
    def Exists(imagePath: str, target: str | uia.Control, anchorsElement: uia.Control | None = None, rect: dict | None = None, accuracy: float = 0.9, searchDelay: int = 10000, continueOnError: bool = False, delayAfter: int = 0, delayBefore: int = 100, setForeground: bool = True, matchType: str = 'GrayMatch', backgroundPic: bool = False) -> bool:
        '''
        判断图像是否存在

        Image.Exists(\'d:\\test.jpg\', target, anchorsElement=None, rect=None, accuracy=0.9, searchDelay=10000, continueOnError=False, delayAfter=0, delayBefore=100, setForeground=True, matchType=\'GrayMatch\', backgroundPic=False)

        :param imagePath:[必选参数]要查找的图片路径
        :param target:[必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param anchorsElement:[可选参数]从哪个元素开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param rect:[可选参数]需要查找的范围，程序会在控件这个范围内进行图片识别，如果范围传递为 None，则进行控件矩形区域范围内的图片识别，如果范围传递为 {"x":10,"y":5,"width":200,"height":100}，则进行控件矩形区域范围内以左上角向右偏移10像素、向下偏移5像素为起点，向右侧200，向下100的范围内的图片识别。默认None
        :param accuracy:[可选参数]查找图片时使用的相似度，相似度范围从 0.5 - 1.0，表示 50% - 100% 相似。默认0.9
        :param searchDelay:[可选参数]超时时间(毫秒)。默认10000
        :param continueOnError:[可选参数]错误继续执行。默认False
        :param delayAfter:[可选参数]执行后延时(毫秒)。默认0
        :param delayBefore:[可选参数]执行前延时(毫秒)。默认100
        :param setForeground:[可选参数]激活窗口。默认True
        :param matchType:[可选参数]指定查找图像的匹配方式，\'GrayMatch\':“灰度匹配”速度快，但在极端情况下可能会匹配失败，\'ColorMatch\':“彩色匹配”相对“灰度匹配”更精准但匹配速度稍慢。默认\'GrayMatch\'
        :param backgroundPic:[可选参数]是否后台识图片（图片需与查找范围在同一窗口）。True为后台识别图片，False为前台识别图片。默认False。
        :return:存在返回True，不存在返回False
        '''
    @staticmethod
    def Find(imagePath: str, target: str | uia.Control, anchorsElement: uia.Control | None = None, rect: dict | None = None, accuracy: int | float = 0.9, searchDelay: int = 10000, continueOnError: bool = False, delayAfter: int = 0, delayBefore: int = 100, setForeground: bool = True, matchType: str = 'GrayMatch', backgroundPic: bool = False, iSerialNo: int = 0, returnPosition: str = 'center') -> dict | list | None:
        '''
        查找图像

        Image.Find(\'d:\\test.jpg\', target, anchorsElement=None, rect=None, accuracy=0.9, searchDelay=10000, continueOnError=False, delayAfter=0, delayBefore=100, setForeground=True, matchType=\'GrayMatch\', backgroundPic=False, iSerialNo=0, returnPosition="center")

        :param imagePath:[必选参数]要查找的图片路径
        :param target:[必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param anchorsElement:[可选参数]从哪个元素开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param rect:[可选参数]需要查找的范围，程序会在控件这个范围内进行图片识别，如果范围传递为 None，则进行控件矩形区域范围内的图片识别，如果范围传递为 {"x":10,"y":5,"width":200,"height":100}，则进行控件矩形区域范围内以左上角向右偏移10像素、向下偏移5像素为起点，向右侧200，向下100的范围内的图片识别。默认None
        :param accuracy:[可选参数]查找图片时使用的相似度，相似度范围从 0.5 - 1.0，表示 50% - 100% 相似。默认0.9
        :param searchDelay:[可选参数]超时时间(毫秒)。默认10000
        :param continueOnError:[可选参数]错误继续执行。默认False
        :param delayAfter:[可选参数]执行后延时(毫秒)。默认0
        :param delayBefore:[可选参数]执行前延时(毫秒)。默认100
        :param setForeground:[可选参数]激活窗口。默认True
        :param matchType:[可选参数]指定查找图像的匹配方式，\'GrayMatch\':“灰度匹配”速度快，但在极端情况下可能会匹配失败，\'ColorMatch\':“彩色匹配”相对“灰度匹配”更精准但匹配速度稍慢。默认\'GrayMatch\'
        :param backgroundPic:[可选参数]是否后台识图片（图片需与查找范围在同一窗口）。True为后台识别图片，False为前台识别图片。默认False。
        :param iSerialNo:[可选参数]指定图像匹配到多个目标时的序号，序号为从1开始的正整数，在屏幕上从左到右从上到下依次递增，匹配到最靠近屏幕左上角的目标序号为1,如果是0，返回所有匹配图像的坐标。默认为0
        :param returnPosition:[可选参数]\'center\':返回图片中心坐标，\'topLeft\':返回图片左上角坐标,\'topRight\':返回图片右上角坐标,\'bottomLeft\':返回图片左下角坐标,\'bottomRight\':返回图片右下角坐标。默认\'center\'
        :return:返回图像的坐标，iSerialNo为0时，返回list，如[{\'x\':100, \'y\':100}, {\'x\':300,\'y\':300}]，iSerialNo大于0时，返回dict，如{\'x\':100, \'y\':100},匹配不到时返回None
        '''
    @staticmethod
    def Click(imagePath: str, target: str | uia.Control, anchorsElement: uia.Control | None = None, rect: dict | None = None, accuracy: float = 0.9, button: str = 'left', clickType: str = 'click', searchDelay: int = 10000, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100, setForeground: bool = True, cursorPosition: str = 'center', cursorOffsetX: int = 0, cursorOffsetY: int = 0, keyModifiers: list = None, simulateType: str = 'simulate', moveSmoothly: bool = False, matchType: str = 'GrayMatch', backgroundPic: bool = False, iSerialNo: int = 1):
        '''
        点击图像

        Image.Click(\'d:\\test.jpg\', target, anchorsElement=None, rect=None, accuracy=0.9, button=\'left\', clickType=\'click\', searchDelay=10000, continueOnError=False, delayAfter=100, delayBefore=100,
             setForeground=True, cursorPosition=\'center\', cursorOffsetX=0, cursorOffsetY=0, keyModifiers=None, simulateType=\'simulate\', moveSmoothly=False, matchType=\'GrayMatch\', backgroundPic=False, iSerialNo=1)

        :param imagePath:[必选参数]要查找的图片路径
        :param target:[必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param anchorsElement:[可选参数]从哪个元素开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param rect:[可选参数]需要查找的范围，程序会在控件这个范围内进行图片识别，如果范围传递为 None，则进行控件矩形区域范围内的图片识别，如果范围传递为 {"x":10,"y":5,"width":200,"height":100}，则进行控件矩形区域范围内以左上角向右偏移10像素、向下偏移5像素为起点，向右侧200，向下100的范围内的图片识别。默认None
        :param accuracy:[可选参数]查找图片时使用的相似度，相似度范围从 0.5 - 1.0，表示 50% - 100% 相似。默认0.9
        :param button:[可选参数]鼠标点击。鼠标左键:"left" 鼠标右键:"right" 鼠标中键:"middle"。默认"left"
        :param clickType:[可选参数]点击类型。单击:"click" 双击:"dbclick" 按下:"down" 弹起:"up"。默认"click"
        :param searchDelay:[可选参数]超时时间(毫秒)。默认10000
        :param continueOnError:[可选参数]错误继续执行。默认False
        :param delayAfter:[可选参数]执行后延时(毫秒)。默认100
        :param delayBefore:[可选参数]执行前延时(毫秒)。默认100
        :param setForeground:[可选参数]激活窗口。默认True
        :param cursorPosition:[可选参数]光标位置。中心:"center" 左上角:"topLeft" 右上角:"topRight" 左下角:"bottomLeft" 右下角:"bottomRight"。默认"center"
        :param cursorOffsetX:[可选参数]横坐标偏移。默认0
        :param cursorOffsetY:[可选参数]纵坐标偏移。默认0
        :param keyModifiers:[可选参数]辅助按键["Alt","Ctrl","Shift","Win"]可多选。默认None
        :param simulateType:[可选参数]操作类型。模拟操作:"simulate" 消息操作:"message"。默认"simulate"
        :param moveSmoothly:[可选参数]是否平滑移动鼠标。默认False
        :param matchType:[可选参数]指定查找图像的匹配方式，\'GrayMatch\':“灰度匹配”速度快，但在极端情况下可能会匹配失败，\'ColorMatch\':“彩色匹配”相对“灰度匹配”更精准但匹配速度稍慢。默认\'GrayMatch\'
        :param backgroundPic:[可选参数]是否后台识图片（图片需与查找范围在同一窗口）。True为后台识别图片，False为前台识别图片。默认False。注意：当simulateType为message时，该字段设置为True才会生效
        :param iSerialNo:[可选参数]指定图像匹配到多个目标时的序号，序号为从1开始的正整数，在屏幕上从左到右从上到下依次递增，匹配到最靠近屏幕左上角的目标序号为1,如果是0，匹配所有图片（即点击所有匹配到的图片）。默认为1
        :return:None
        '''
    @staticmethod
    def Hover(imagePath: str, target: str | uia.Control, anchorsElement: uia.Control | None = None, rect: dict | None = None, accuracy: float = 0.9, searchDelay: int = 10000, continueOnError: bool = False, delayAfter: int = 100, delayBefore: int = 100, setForeground: bool = True, cursorPosition: str = 'center', cursorOffsetX: int = 0, cursorOffsetY: int = 0, keyModifiers: list = None, moveSmoothly: bool = False, matchType: str = 'GrayMatch', backgroundPic: bool = False, iSerialNo: int = 1):
        '''
        鼠标移动到图像上

        Image.Hover(\'d:\\test.jpg\', target, anchorsElement=None, rect=None, accuracy=0.9, searchDelay=10000, continueOnError=False, delayAfter=100, delayBefore=100,
             setForeground=True, cursorPosition=\'center\', cursorOffsetX=0, cursorOffsetY=0, keyModifiers=None, moveSmoothly=False, matchType=\'GrayMatch\', backgroundPic=False, iSerialNo=1)

        :param imagePath:[必选参数]要查找的图片路径
        :param target:[必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param anchorsElement:[可选参数]从哪个元素开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param rect:[可选参数]需要查找的范围，程序会在控件这个范围内进行图片识别，如果范围传递为 None，则进行控件矩形区域范围内的图片识别，如果范围传递为 {"x":10,"y":5,"width":200,"height":100}，则进行控件矩形区域范围内以左上角向右偏移10像素、向下偏移5像素为起点，向右侧200，向下100的范围内的图片识别。默认None
        :param accuracy:[可选参数]查找图片时使用的相似度，相似度范围从 0.5 - 1.0，表示 50% - 100% 相似。默认0.9
        :param searchDelay:[可选参数]超时时间(毫秒)。默认10000
        :param continueOnError:[可选参数]错误继续执行。默认False
        :param delayAfter:[可选参数]执行后延时(毫秒)。默认100
        :param delayBefore:[可选参数]执行前延时(毫秒)。默认100
        :param setForeground:[可选参数]激活窗口。默认True
        :param cursorPosition:[可选参数]光标位置。中心:"center" 左上角:"topLeft" 右上角:"topRight" 左下角:"bottomLeft" 右下角:"bottomRight"。默认"center"
        :param cursorOffsetX:[可选参数]横坐标偏移。默认0
        :param cursorOffsetY:[可选参数]纵坐标偏移。默认0
        :param keyModifiers:[可选参数]辅助按键["Alt","Ctrl","Shift","Win"]可多选。默认None
        :param moveSmoothly:[可选参数]是否平滑移动鼠标。默认False
        :param matchType:[可选参数]指定查找图像的匹配方式，\'GrayMatch\':“灰度匹配”速度快，但在极端情况下可能会匹配失败，\'ColorMatch\':“彩色匹配”相对“灰度匹配”更精准但匹配速度稍慢。默认\'GrayMatch\'
        :param backgroundPic:[可选参数]是否后台识图片（图片需与查找范围在同一窗口）。True为后台识别图片，False为前台识别图片。默认False。
        :param iSerialNo:[可选参数]指定图像匹配到多个目标时的序号，序号为从1开始的正整数，在屏幕上从左到右从上到下依次递增，匹配到最靠近屏幕左上角的目标序号为1,如果是0，匹配所有图片（即鼠标将移动经过所有匹配到的图片）。默认为1
        :return:None
        '''
    @staticmethod
    def Wait(imagePath: str, target: str | uia.Control, anchorsElement: uia.Control | None = None, rect: dict | None = None, accuracy: float = 0.9, waitType: str = 'show', searchDelay: int = 10000, continueOnError: bool = False, delayAfter: int = 0, delayBefore: int = 100, setForeground: bool = True, matchType: str = 'GrayMatch', backgroundPic: bool = False):
        '''
        等待图像显示或消失

        Image.Wait(\'d:\\test.jpg\', target, anchorsElement=None, rect=None, accuracy=0.9, waitType="show", searchDelay=10000, continueOnError=False, delayAfter=0, delayBefore=100, setForeground=True, matchType=\'GrayMatch\', backgroundPic=False)

        :param imagePath:[必选参数]要查找的图片路径
        :param target:[必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param anchorsElement:[可选参数]从哪个元素开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param rect:[可选参数]需要查找的范围，程序会在控件这个范围内进行图片识别，如果范围传递为 None，则进行控件矩形区域范围内的图片识别，如果范围传递为 {"x":10,"y":5,"width":200,"height":100}，则进行控件矩形区域范围内以左上角向右偏移10像素、向下偏移5像素为起点，向右侧200，向下100的范围内的图片识别。默认None
        :param accuracy:[可选参数]查找图片时使用的相似度，相似度范围从 0.5 - 1.0，表示 50% - 100% 相似。默认0.9
        :param waitType:[可选参数]等待方式。 等待显示："show" 等待消失:"hide"。默认"show"
        :param searchDelay:[可选参数]超时时间(毫秒)。默认10000
        :param continueOnError:[可选参数]错误继续执行。默认False
        :param delayAfter:[可选参数]执行后延时(毫秒)。默认0
        :param delayBefore:[可选参数]执行前延时(毫秒)。默认100
        :param setForeground:[可选参数]激活窗口。默认True
        :param matchType:[可选参数]指定查找图像的匹配方式，\'GrayMatch\':“灰度匹配”速度快，但在极端情况下可能会匹配失败，\'ColorMatch\':“彩色匹配”相对“灰度匹配”更精准但匹配速度稍慢。默认\'GrayMatch\'
        :param backgroundPic:[可选参数]是否后台识图片（图片需与查找范围在同一窗口）。True为后台识别图片，False为前台识别图片。默认False。
        :return:None
        '''
    @staticmethod
    def ComColor(color: str, target: str | uia.Control, anchorsElement: uia.Control | None = None, searchDelay: int = 10000, continueOnError: bool = False, delayAfter: int = 0, delayBefore: int = 100, setForeground: bool = True, beginPosition: str = 'center', positionOffsetX: int = 0, positionOffsetY: int = 0, backgroundPic: bool = False):
        '''
        目标内指定位置比色

        Image.ComColor(\'FF0000\', target, anchorsElement=None, searchDelay=10000, continueOnError=False, delayAfter=0, delayBefore=100, setForeground=True, beginPosition=\'center\', positionOffsetX=0, positionOffsetY=0, backgroundPic=False)

        :param color:[必选参数]指定位置是否为此颜色，十六进制颜色，RGB色值，例如："FF0000"，支持偏色，如"FF0000-101010"
        :param target:[必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param anchorsElement:[可选参数]从哪个元素开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param searchDelay:[可选参数]超时时间(毫秒)。默认10000
        :param continueOnError:[可选参数]错误继续执行。默认False
        :param delayAfter:[可选参数]执行后延时(毫秒)。默认0
        :param delayBefore:[可选参数]执行前延时(毫秒)。默认100
        :param setForeground:[可选参数]激活窗口。默认True
        :param beginPosition:[可选参数]起始位置。center:中心, topLeft:左上角, topRight:右上角, bottomLeft:左下角, bottomRight:右下角。默认"center"
        :param positionOffsetX:[可选参数]横坐标偏移。默认0
        :param positionOffsetY:[可选参数]纵坐标偏移。默认0
        :param backgroundPic:[可选参数]是否后台识图片（指定位置的颜色与查找范围在同一窗口）。True为后台识别图片，False为前台识别图片。默认False。
        :return:匹配返回True，不匹配返回False
        '''
    @staticmethod
    def GetColor(target, anchorsElement: Incomplete | None = None, searchDelay: int = 10000, continueOnError: bool = False, delayAfter: int = 0, delayBefore: int = 100, setForeground: bool = True, beginPosition: str = 'center', positionOffsetX: int = 0, positionOffsetY: int = 0, backgroundPic: bool = False):
        '''
        获取目标指定位置的颜色值（16进制RGB字符）

        Image.GetColor(target, anchorsElement=None, searchDelay=10000, continueOnError=False, delayAfter=0, delayBefore=100, setForeground=True, beginPosition=\'center\', positionOffsetX=0, positionOffsetY=0, backgroundPic=False)

        :param target:[必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param anchorsElement:[可选参数]从哪个元素开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param searchDelay:[可选参数]超时时间(毫秒)。默认10000
        :param continueOnError:[可选参数]错误继续执行。默认False
        :param delayAfter:[可选参数]执行后延时(毫秒)。默认0
        :param delayBefore:[可选参数]执行前延时(毫秒)。默认100
        :param setForeground:[可选参数]激活窗口。默认True
        :param beginPosition:[可选参数]起始位置。中心:"center" 左上角:"topLeft" 右上角:"topRight" 左下角:"bottomLeft" 右下角:"bottomRight"。默认"center"
        :param positionOffsetX:[可选参数]横坐标偏移。默认0
        :param positionOffsetY:[可选参数]纵坐标偏移。默认0
        :param backgroundPic:[可选参数]是否后台识图片（图片需与查找范围在同一窗口）。True为后台识别图片，False为前台识别图片。默认False。
        :return:返回颜色值（16进制的RGB字符），如"FF0000"
        '''
    @staticmethod
    def FindColor(colors: str, target: str | uia.Control, anchorsElement: uia.Control | None = None, rect: dict | None = None, searchDelay: int = 10000, continueOnError: bool = False, delayAfter: int = 0, delayBefore: int = 100, setForeground: bool = True, backgroundPic: bool = False, returnNum: str = 'first', relativeType: str = 'screen'):
        '''
        查找颜色

        Image.FindColor(\'FF0000\', target, anchorsElement=None, rect=None, searchDelay=10000, continueOnError=False, delayAfter=0, delayBefore=100, setForeground=True, backgroundPic=False, returnNum=\'first\', relativeType=\'screen\')

        :param colors: [必选参数]需要查找的颜色值字符串，十六进制颜色，支持偏色，支持同时多个颜色，例如 "FF0000" 或 "FF0000-101010" 或 "FF0000-101010|0000FF-101010"
        :param target:[必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param anchorsElement:[可选参数]从哪个元素开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param rect:[可选参数]需要查找的范围，程序会在控件这个范围内进行颜色识别，如果范围传递为 None，则进行控件矩形区域范围内的颜色识别，如果范围传递为 {"x":10,"y":5,"width":200,"height":100}，则进行控件矩形区域范围内以左上角向右偏移10像素、向下偏移5像素为起点，向右侧200，向下100的范围内的颜色识别。默认None
        :param searchDelay:[可选参数]超时时间(毫秒)。默认10000
        :param continueOnError:[可选参数]错误继续执行。默认False
        :param delayAfter:[可选参数]执行后延时(毫秒)。默认0
        :param delayBefore:[可选参数]执行前延时(毫秒)。默认100
        :param setForeground:[可选参数]激活窗口。默认True
        :param backgroundPic:[可选参数]是否后台识图片（颜色需与查找范围在同一窗口）。True为后台识别图片，False为前台识别图片。默认False。
        :param returnNum:[可选参数]坐标返回数量。first:返回找到的第一个颜色坐标, all:返回找到的所有颜色坐标。默认first，查找顺序是从上到下，从左到右。
        :param relativeType:[可选参数]查找坐标相对类型。screen:返回相对屏幕的坐标，以屏幕左上角0,0为坐标原点。 image:返回相对查找范围的坐标，以查找范围的左上角0,0为坐标原点。默认screen
        :return:返回颜色的坐标，当returnNum为first时，返回如[50 100], 当returnNum为all时，返回如[[50 100],[50,101],[51,100]...], 找不到时返回None
        '''
    @staticmethod
    def FindMultColor(colorDes: str, target: str | uia.Control, anchorsElement: uia.Control | None = None, rect: dict | None = None, accuracy: int | float = 1.0, searchDelay: int = 10000, continueOnError: bool = False, delayAfter: int = 0, delayBefore: int = 100, setForeground: bool = True, backgroundPic: bool = False, relativeType: str = 'screen'):
        '''
        多点找色

        Image.FindMultColor(colorDes, target, anchorsElement=None, rect=None, accuracy=1.0, searchDelay=10000, continueOnError=False, delayAfter=0, delayBefore=100, setForeground=True, backgroundPic=False, relativeType=\'screen\')

        :param colorDes:[必选参数]多点颜色描述，如"40b7ff-101010,-16|-14|58c0ff-101010,-17|5|4ebbff-101010,17|-3|26adff-101010,17|15|42b7ff-101010", 解释：以40b7ff-101010颜色为锚点，符合向左偏移16像素，向上偏移14像素，且颜色符合58c0ff-101010，向...向...且颜色符合...等等。推荐使用<大漠综合工具>获取颜色描述
        :param target:[必选参数]tdRPA拾取器获取的目标元素特征字符串或uia目标元素对象
        :param anchorsElement:[可选参数]从哪个元素开始找，不传则从桌面顶级元素开始找（有值可提高查找速度）。默认None
        :param rect:[可选参数]需要查找的范围，程序会在控件这个范围内进行多点找色，如果范围传递为 None，则进行控件矩形区域范围内的多点找色，如果范围传递为 {"x":10,"y":5,"width":200,"height":100}，则进行控件矩形区域范围内以左上角向右偏移10像素、向下偏移5像素为起点，向右侧200，向下100的范围内的多点找色。默认None
        :param accuracy:[可选参数]多点找色时使用的相似度，相似度范围从 0.5 - 1.0，表示 50% - 100% 相似。默认1.0
        :param searchDelay:[可选参数]超时时间(毫秒)。默认10000
        :param continueOnError:[可选参数]错误继续执行。默认False
        :param delayAfter:[可选参数]执行后延时(毫秒)。默认0
        :param delayBefore:[可选参数]执行前延时(毫秒)。默认100
        :param setForeground:[可选参数]激活窗口。默认True
        :param backgroundPic:[可选参数]是否后台识图片（颜色描述需与查找范围在同一窗口）。True为后台识别图片，False为前台识别图片。默认False。
        :param relativeType:[可选参数]查找坐标相对类型。screen:返回相对屏幕的坐标，以屏幕左上角0,0为坐标原点。 image:返回相对查找范围的坐标，以查找范围的左上角0,0为坐标原点。默认screen
        :return:返回找到的坐标，如{"x":int, "y":int}。找不到返回None
        '''

