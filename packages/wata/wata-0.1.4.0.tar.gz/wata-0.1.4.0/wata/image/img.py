from wata.image.utils import utils
from pathlib import Path
from typing import Union

class ImageProcess:
    @staticmethod
    def show_img(path:Union[str, Path]):
        '''
        **功能描述**: 展示图像  
        
        Args:
            path: 图像路径  

        Returns:
            无  
        '''
        utils.show_img(path)

    @staticmethod
    def img2video(img_dir, save_path, fps=30):
        '''
        **功能描述**: 将图像连成视频  
        
        Args:
            img_dir: 图像目录的路径  
            save_path: 视频保存地址  
            fps: 视频帧率,默认30  

        Returns:  
            无  
        '''
        utils.images_to_video(img_dir, save_path, fps)

    @staticmethod
    def video2img(path, save_path):
        '''
        **功能描述**: 将视频展开成图像  
        
        Args:
            path: 视频地址  
            save_path: 图像保存地址  

        Returns:
            无  
        '''
        utils.video_to_images(path, save_path)
