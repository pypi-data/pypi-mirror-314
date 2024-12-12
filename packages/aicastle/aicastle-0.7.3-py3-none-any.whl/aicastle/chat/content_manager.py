from PIL import Image
import base64
from io import BytesIO
import os
import fitz  # PyMuPDF
from aicastle.chat.tokens import split_tokens
import aicastle.chat.hparams as chat_hp

default_system_text = chat_hp.system_text
default_assistant_guidelines = chat_hp.assistant_guidelines

class OpenAIContentManager:
    def __init__(self, target, img_max = 1024, dpi = 90):
        self.thumbnail_size = (img_max, img_max)
        self.dpi = dpi

        if isinstance(target, str):     # 파일 경로에서 가져오기 (ex) path/to/image.jpg
            self.data = self.loader(target)
            self.filepath = target
        elif isinstance(target, dict):  # 완성된 content data (ex) {"type":"image_url", "data":"https://..."}
            self.data = target
            self.filepath = None
        else :
            raise Exception(f"Invalid target : {type(target)}")
        
        self.type = self.data["type"] if self.data else None

    def get_incontext_messages(self, model="gpt-4o", max_tokens=50000, in_text=True, in_image=False, info_modified=False):
        if info_modified :
            content = [
                {"type":"text", "text":"(info) 다음 파일이 수정 됨."}
            ]
        else :
            content = []
        
        
        if self.type == "text":
            if in_text :
                content += \
                    [{"type":"text", "text":f'''<<<context filepath="{self.filepath}">>>'''}] +\
                    [{"type":"text", "text":tokens} for tokens in split_tokens(self.data["data"], max_tokens, model=model)] +\
                    [{"type":"text", "text":f'''<<<///context>>>'''}]
            else :
                content.append({"type":"text", "text":f'''<<<context filepath="{self.filepath}"///>>>'''})
        elif self.type == "image_url":
            if in_image :
                content += [
                    {"type":"text", "text":f'''<<<context filepath="{self.filepath}">>>'''},
                    {"type":"image_url", "image_url":{"url":self.data["data"]}},
                    {"type":"text", "text":f'''<<<///context>>>'''}
                ]
            else :
                content.append({"type":"text", "text":f'''<<<context filepath="{self.filepath}"///>>>'''})
        elif self.type == "pdf_pages":
            if in_text or in_image :
                for page_data in self.data["data"]:
                    content.append({"type":"text", "text":f'''<<<context filepath="{self.filepath}" page_num="{page_data["page_num"]}">>>'''})
                    if in_text :
                        for tokens in split_tokens(page_data["text"], max_tokens, model=model):
                            content.append({"type":"text", "text":tokens})
                    if in_image :
                        content.append({"type":"image_url", "image_url":{"url":page_data["image_url"]}})
                    content.append({"type":"text", "text":f'''<<<///context>>>'''})
            else :
                content.append({"type":"text", "text":f'''<<<context filepath="{self.filepath}"///>>>'''})
        else :
            content.append({"type":"text", "text":f'''<<<context filepath="{self.filepath}"///>>>'''})
        
        messages = [{"role":"user", "content":content}]
        return messages
    
    def get_finetuning_data(self, system_text=default_system_text, max_tokens=16000, model="gpt-4o", in_text=True, in_image=False):
        system_message = {"role":"system", "content":[{"type":"text", "text":system_text}]}
        finetuning_data = []

        #### 가이드라인 학습

        #### 데이터 학습
        if self.type == "text":
            if in_text :
                messages = [
                    system_message,
                    {"role":"user", "content": [{"type":"text", "text":"파일경로 중 하나를 작성하시오."}]},
                    {"role":"assistant", "content": [{"type":"text", "text":self.filepath}]},
                ]
                tokens_list = split_tokens(self.data["data"], max_tokens, model=model)
                if len(tokens_list) > 0 :
                    messages.append({"role":"user", "content": [{"type":"text", "text":"이 파일의 내용을 작성하시오."}]})
                    messages += [{"role":"assistant", "content": [{"type":"text", "text":tokens}]} for tokens in tokens_list]
                
                finetuning_data.append({"messages":messages})
        elif self.type == "image_url" :
            if in_image :
                messages = [
                    system_message,
                    {"role":"user", "content": [{"type":"text", "text":"다음 이미지의 파일경로를 작성하시오."}, {"type":"image_url", "image_url":{"url":self.data["data"]}}]},
                    {"role":"assistant", "content": [{"type":"text", "text":self.filepath}]},
                ]
                finetuning_data.append({"messages":messages})
        elif self.type == "pdf_pages":
            ### 메세지 경로 맞추기
            messages = [
                system_message,
                {"role":"user", "content": [{"type":"text", "text":"파일경로 중 하나를 작성하시오."}]},
                {"role":"assistant", "content": [{"type":"text", "text":self.filepath}]},
                {"role":"user", "content": [{"type":"text", "text":"이 파일의 총 페이지 수를 작성하시오."}]},
                {"role":"assistant", "content": [{"type":"text", "text":str(len(self.data["data"]))}]},
            ]
            finetuning_data.append({"messages":messages})
            ### 페이지 내용 맞추기 (텍스트)
            if in_text :
                for page_data in self.data["data"]:
                    tokens_list = split_tokens(page_data["text"], max_tokens, model=model)
                    if len(tokens_list) > 0 :
                        messages = [
                            system_message,
                            {"role":"user", "content": [{"type":"text", "text":f"{self.filepath} 파일의 {page_data["page_num"]} 페이지에서 추출된 텍스트를 작성하시오."}]},
                        ]
                        messages += [{"role":"assistant", "content": [{"type":"text", "text":tokens}]} for tokens in tokens_list]
                        finetuning_data.append({"messages":messages})
            ### 페이지 내용 맞추기 (이미지)
            if in_image :
                for page_data in self.data["data"]:
                    messages = [
                        system_message,
                        {"role":"user", "content": [{"type":"text", "text":"다음 이미지의 파일경로를 작성하시오."}, {"type":"image_url", "image_url":{"url":self.data["data"]}}]},
                        {"role":"assistant", "content": [{"type":"text", "text":f"{self.filepath} 파일의 {page_data["page_num"]} 페이지"}]}
                    ]
                    finetuning_data.append({"messages":messages})
        return finetuning_data

    def loader(self, filepath):
        # 텍스트 파일
        try :
            with open(filepath, 'r') as file:
                text = file.read()  # 파일 전체 읽기
                return {"type":"text", "data":text}
        except :
            pass

        # 이미지 파일
        try :
            with Image.open(filepath) as img:
                img.thumbnail(self.thumbnail_size)
                with BytesIO() as buffer:
                    img.save(buffer, format=img.format)
                    base64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
                    mime_type = f"image/{img.format.lower()}"
                    base64_str_url = f"data:{mime_type};base64,{base64_str}"
                    return {"type":"image_url", "data":{"url":base64_str_url}}
        except :
            pass

        # pdf 파일
        if os.path.splitext(filepath)[-1].lower() == '.pdf':
            try : 
                pdf = fitz.open(filepath)
                pdf_pages = []
                for page_idx, page in enumerate(pdf) :
                    pixmap = page.get_pixmap(dpi=self.dpi)
                    pixmap_bytes = pixmap.tobytes()
                    page_image_buffer = BytesIO(pixmap_bytes)
                    with Image.open(page_image_buffer) as img:
                        with BytesIO() as buffer:
                            img.save(buffer, format="PNG")  # PDF 페이지는 PNG 형식으로 저장
                            base64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
                            mime_type = "image/png"
                            base64_str_url = f"data:{mime_type};base64,{base64_str}"
                    
                    pdf_pages.append({"page_num":page_idx + 1, "text":page.get_text(), "image_url":base64_str_url})
                pdf.close()
                return {"type":"pdf_pages", "data":pdf_pages}
            except :
                pass
        
        # 지원되지 않는 파일
        return None
