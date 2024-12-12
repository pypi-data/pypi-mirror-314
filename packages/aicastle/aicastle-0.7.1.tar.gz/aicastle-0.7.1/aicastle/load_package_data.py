import pkg_resources
from PIL import Image
from io import BytesIO

class PackageImageLoader:
    def __init__(self, package_image_path):
        self.package_image_path = package_image_path
        self.image_path = self.get_image_path()
        # self.image = self.load_image()
    
    def get_image_path(self):
        # 패키지 내 데이터 파일 경로
        return pkg_resources.resource_filename(__name__, f'package_data/{self.package_image_path}')
    
    def load_image(self):
        # 이미지 열기
        with open(self.image_path, 'rb') as img_file:
            image_data = img_file.read()
        image = Image.open(BytesIO(image_data))
        return image