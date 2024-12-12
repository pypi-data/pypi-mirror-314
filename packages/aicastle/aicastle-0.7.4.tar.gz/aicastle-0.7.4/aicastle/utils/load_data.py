import os
import requests
from PIL import Image
import base64
from io import BytesIO

class ImageLoader:
    def __init__(self, target, format=None):
        self.image = self.load_image(target)
        if not self.image:
            raise ValueError("이미지를 로드할 수 없습니다.")
        self.format = format if format else self.image.format
        self.base64_str = self.get_base64_str()
        self.base64_str_url = self.get_base64_str_url()
    
    def load_image(self, target):
        if isinstance(target, Image.Image) :
            return target
        elif isinstance(target, str):
            # 파일 경로에서 로드
            try :
                image = Image.open(target)
                return image
            except :
                pass
            
            # URL에서 로드
            try :
                response = requests.get(target)
                image_data = BytesIO(response.content)
                image = Image.open(image_data)
                return image
            except :
                pass
            
            # base64 문자열에서 로드
            try :
                image_data = BytesIO(base64.b64decode(target))
                image = Image.open(image_data)
                return image
            except :
                pass
        else :
            raise Exception("Invalid target")
    
    def get_base64_str(self):
        with BytesIO() as buffer:
            self.image.save(buffer, format=self.format)
            base64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return base64_str
    
    def get_base64_str_url(self):
        mime_type = f"image/{self.format.lower()}"
        return f"data:{mime_type};base64,{self.base64_str}"
        
    def convert(self, format=None, size=None, max_size=None):
        converted_format = format if format else self.format
        converted_image = self.image.copy()
        if converted_format != self.format  :
            if converted_format == 'JPEG':
                converted_image = converted_image.convert('RGB')
            elif converted_format == 'GIF':
                converted_image = converted_image.convert('P', palette=Image.ADAPTIVE)
            elif converted_format == 'PNG':
                converted_image = converted_image.convert('RGBA')
            else :
                raise Exception("Invalid format")
        if size :
            converted_image = converted_image.resize(size)
        elif max_size:
            width, height = converted_image.size
            if max(width, height) > max_size:
                if width > height:
                    new_width = max_size
                    new_height = int((max_size / width) * height)
                else:
                    new_height = max_size
                    new_width = int((max_size / height) * width)
                converted_image = converted_image.resize((new_width, new_height))
        return ImageLoader(converted_image, format=converted_format)

    def show(self):
        self.image.show()

    def save_image(self, save_path):
        self.image.save(save_path, format=self.format)