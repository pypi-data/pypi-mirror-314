import tiktoken
import aicastle.chat.hparams as chat_hp

default_model = chat_hp.model
default_max_tokens = chat_hp.max_tokens
default_chat_token_price = chat_hp.chat_token_price
default_finetuning_token_price = chat_hp.finetuning_token_price


def calculate_tokens(text: str, model: str = default_model, return_count=True):
    try:  # 모델에 맞는 토크나이저 가져오기
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:  # 기본 토크나이저 (호환되지 않는 모델의 경우)
        encoding = tiktoken.get_encoding("cl100k_base")

    tokens = encoding.encode(text)
    if return_count :
        return len(tokens)
    else :
        return tokens


def split_tokens(text: str, max_tokens: int = default_max_tokens, model: str = default_model):
    tokens = calculate_tokens(text, model=model, return_count=False)
    encoding = tiktoken.encoding_for_model(model)
    chunks = [tokens[i:i + max_tokens] for i in range(0, len(tokens), max_tokens)]
    return [encoding.decode(chunk) for chunk in chunks]


def calculate_openai_messages_tokens_price(messages, model=default_model, token_price=default_chat_token_price):
    tokens_count = 0
    for message in messages :
        for content in message["content"]:
            if isinstance(content, str) :
                tokens_count += calculate_tokens(content, model, return_count=True)
            elif isinstance(content, dict):
                if content["type"] == "text":
                    tokens_count += calculate_tokens(content["text"], model, return_count=True)
                else :
                    # 이미지 토큰 계산 추후 업데이트
                    pass
            else :
                raise Exception(f"Invalid content type : {type(content)}")
    total_price = tokens_count * token_price
    return tokens_count, total_price


def calculate_openai_finetuning_messages_tokens_price(finetuning_data, model=default_model, token_price=default_finetuning_token_price):
    tokens_count = 0
    for messages in finetuning_data:
        for message in messages["messages"] :
            for content in message["content"]:
                if isinstance(content, str) :
                    tokens_count += calculate_tokens(content, model, return_count=True)
                elif isinstance(content, dict):
                    if content["type"] == "text":
                        tokens_count += calculate_tokens(content["text"], model, return_count=True)
                    else :
                        # 이미지 토큰 계산 추후 업데이트
                        pass
                else :
                    raise Exception(f"Invalid content type : {type(content)}")
    total_price = tokens_count * token_price
    return tokens_count, total_price