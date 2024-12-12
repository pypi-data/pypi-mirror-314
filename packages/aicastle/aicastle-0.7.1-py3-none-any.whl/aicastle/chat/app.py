from dotenv import load_dotenv
import streamlit as st

from aicastle.chat.utils import get_chat_file_hashes
from aicastle.chat.content_manager import OpenAIContentManager
from aicastle.chat.utils import load_config
import aicastle.chat.function_call as fc
from aicastle.chat.client import get_client, OpenAIChatManager
from aicastle.chat.tokens import (
    calculate_openai_messages_tokens_price,
    calculate_openai_finetuning_messages_tokens_price
)
load_dotenv(
    dotenv_path='.aicastle/chat/.env', 
    override=True  # 환경변수 덮어쓰기
)

config_data = load_config()

####### streamlit
st.title("AI Castle. Workspace Chat")

if "chat_file_hashes" not in st.session_state:
    chat_file_hashes = get_chat_file_hashes()
    st.session_state["chat_file_hashes"] = chat_file_hashes
else :
    chat_file_hashes = st.session_state["chat_file_hashes"]

if "chat_manager" not in st.session_state:
    incontext_messages = []
    for filepath in chat_file_hashes :
        content_manager = OpenAIContentManager(filepath)
        incontext_messages += content_manager.get_incontext_messages(
            model = config_data["model"],
            max_tokens = config_data["incontext"]["max_tokens"],
            in_text = config_data["incontext"]["in_text"],
            in_image = config_data["incontext"]["in_image"],
            info_modified = False,
        )
    tokens_count, total_price = calculate_openai_messages_tokens_price(incontext_messages)
    print(" ============ incontext_messages (only text) ============ ")
    print(f"tokens_count: {tokens_count} / total_price: {total_price}")

    chat_manager = OpenAIChatManager(
        platform = config_data["platform"],
        chat_type = config_data["chat_type"],
        model = config_data["model"],
        temperature = config_data["temperature"],
        top_p = config_data["top_p"],
        stream = config_data["stream"],
        api_version = config_data["api_version"],
        additional_system_text = config_data["additional_system_text"],
        messages = incontext_messages,
        function_module=fc,
    )
    st.session_state["chat_manager"] = chat_manager
else :
    chat_manager = st.session_state["chat_manager"]

if "show_messages" not in st.session_state:
    show_messages = []
    st.session_state["show_messages"] = show_messages
else :
    show_messages = st.session_state["show_messages"]

for message in show_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"][0]["text"])


if user_input := st.chat_input("What is up?"):
    ### 유저 입력
    user_message = {"role": "user", "content": [{"type": "text","text": user_input}]}
    show_messages.append(user_message)
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.spinner('Processing...'):  # 스피너 시작
        ### 파일 변경 감지
        new_chat_file_hashes = get_chat_file_hashes()
        new_incontext_messages = []
        for filepath, file_hash in new_chat_file_hashes.items() :
            if (not filepath in chat_file_hashes) or (chat_file_hashes[filepath] != file_hash):
                chat_file_hashes[filepath] = file_hash
                content_manager = OpenAIContentManager(filepath)
                new_incontext_messages += content_manager.get_incontext_messages(
                    model = config_data["model"],
                    max_tokens = config_data["incontext"]["max_tokens"],
                    in_text = config_data["incontext"]["in_text"],
                    in_image = config_data["incontext"]["in_image"],
                    info_modified = True,
                )
        if new_incontext_messages :
            chat_manager.add_messages(new_incontext_messages)

        ### 유저 request
        result_container = chat_manager.create([user_message])

        ### assistant response
        with st.chat_message("assistant"):
            assistant_content_box = st.empty()
            assistant_content = ""
            while True :
                if result_container['done'] and (len(result_container['texts']) == 0):
                    break
                else :
                    try :
                        text = result_container["texts"].pop(0)
                        assistant_content += text
                        assistant_content_box.markdown(assistant_content)
                    except :
                        pass
            
            ### submit_tool
            while result_container['tool_call_need'] :
                assistant_content += "\n---\nfunction_calling ....\n\n---\n"
                assistant_content_box.markdown(assistant_content)
                result_container = chat_manager.submit_tool_outputs(result_container['run'])
                while True :
                    if result_container['done'] and (len(result_container['texts']) == 0):
                        break
                    else :
                        try :
                            text = result_container["texts"].pop(0)
                            assistant_content += text
                            assistant_content_box.markdown(assistant_content)
                        except :
                            pass
        
            assistant_message = {"role": "assistant", "content": [{"type": "text","text": assistant_content}]}
            show_messages.append(assistant_message)