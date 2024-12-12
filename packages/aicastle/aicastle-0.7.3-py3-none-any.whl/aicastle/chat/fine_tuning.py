import os
import json
from datetime import datetime, timezone
import aicastle.chat.hparams as chat_hp

default_finetuning_folder_path = chat_hp.finetuning_folder_path

def get_utc_now():
    utc_now = datetime.now(timezone.utc)
    return utc_now.strftime("%Y-%m-%dT%H-%M-%SZ")


def save_finetuning_data(finetuning_data, filename=None, save_folder=default_finetuning_folder_path):
    os.makedirs(save_folder, exist_ok=True)

    if filename is None:
        filename = f"{get_utc_now()}.jsonl"  # 기본 파일 이름

    file_path = os.path.join(save_folder, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        for example in finetuning_data:
            f.write(json.dumps(example, ensure_ascii=False) + "\n")

    return file_path
