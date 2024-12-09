from wata.display.utils import utils

class Display:
    
    @staticmethod
    def print(content,type="r"):
        '''
        **功能描述**: 特色打印
        
        Args:
            content: 内容  
            type: 类型支持 字母r g b y p 代表颜色,rr表示粗体,r_表示红色下划线,rx表示红色斜体  

        Returns:
            无  
        '''
        return utils.wataprint(content,type)