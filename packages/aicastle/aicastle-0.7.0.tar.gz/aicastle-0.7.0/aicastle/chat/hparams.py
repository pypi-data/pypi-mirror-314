system_text = "You are the workspace chatbot of aicastle."

assistant_guidelines = [
"""

""".strip(),
]

finetuning_folder_path = ".aicastle/chat/finetuning"

model = "gpt-4o"
max_tokens = 16000
chat_token_price = 0.0035       # 1개 토큰 당 원화
finetuning_token_price = 0.035  # 1개 토큰 당 원화

max_thread_create_len = 32
message_create_workers = 20