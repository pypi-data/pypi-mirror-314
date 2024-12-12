from openai import OpenAI, AzureOpenAI
import inspect
import aicastle.chat.hparams as chat_hp
import aicastle.chat.function_call as fc
import os
from openai.types.beta.assistant_stream_event import ThreadMessageDelta,ThreadRunRequiresAction
from openai.types.beta.threads.text_delta_block import TextDeltaBlock
import json
from concurrent.futures import ThreadPoolExecutor
import threading

def get_client(platform, api_version=None):
    if platform == 'openai':
        client = OpenAI(
            # api_key = os.environ["OPENAI_API_KEY"]
        )
        return client
    elif platform == 'azure_openai':
        client = AzureOpenAI(
            api_version=api_version,
            # api_key=os.environ["AZURE_OPENAI_API_KEY"],
            # azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        )
        return client
    else :
        raise Exception(f"Invalid platform : {platform}")

def get_tools(function_module=fc):
    function_names = [attr for attr in dir(function_module) if callable(getattr(function_module, attr))]
    return [
        {
            "type": "function",
            "function": {
                "name": function_name,
                "description": inspect.getsource(getattr(function_module, function_name))
            }
        }
        for function_name in function_names
    ]

class OpenAIChatManager:
    def __init__(self, 
            platform="openai", 
            chat_type="assistant", 
            model="gpt-4o",
            temperature=1,
            top_p=1,
            stream=True,
            additional_system_text="",
            api_version=None, 
            messages=None,
            function_module=None,
            response=True,
        ):
        self.platform = platform
        self.chat_type = chat_type
        self.additional_system_text = additional_system_text if additional_system_text else ""
        self.stream = stream
        self.function_module = function_module
        self.client = get_client(self.platform, api_version)
        self.response = response

        messages = [] if messages is None else messages.copy()
        if self.chat_type == "assistant":
            self.set_assistant(model, additional_system_text, messages, temperature, top_p, function_module)
        elif self.chat_type == "chat":
            self.set_chat(model, additional_system_text, messages, temperature, top_p, stream, function_module)

        if self.response :
            self.response_list = []

    def run_control(self, run, async_=True, result_container=None):
        if async_ :
            result_container = {"texts":[], "run":None, "tool_call_need":None, "done":False}
            async_thread = threading.Thread(target=self.run_control, kwargs={"run":run, "async_": False, "result_container":result_container})
            result_container["async_thread"] = async_thread
            async_thread.start()
            return result_container

        else :
            if result_container is None :
                result_container = {"texts":[], "run":None, "tool_call_need":None, "done":False}
            
            if self.chat_type == "assistant":
                if self.stream :
                    for event in run:
                        # self.response_list.append(event)
                        # 응답 메세지 출력
                        if isinstance(event, ThreadMessageDelta):
                            if isinstance(event.data.delta.content[0], TextDeltaBlock):
                                result_container["texts"].append(event.data.delta.content[0].text.value)
                    
                    # run
                    result_container["run"] = event.data

                    # tool_call_need
                    if isinstance(event, ThreadRunRequiresAction):
                        result_container["tool_call_need"] = True
                    else :
                        result_container["tool_call_need"] = False

                else :
                    # 응답 메세지 출력
                    messages = self.client.beta.threads.messages.list(thread_id=self.thread_kwargs["thread_id"], run_id=run.id)
                    # self.messages = messages
                    if messages.data :
                        result_container["texts"].append(messages.data[0].content[0].text.value)

                    # run
                    result_container["run"] = run

                    # tool_call_need
                    if run.status == 'requires_action':
                        result_container["tool_call_need"] = True
                    else :
                        result_container["tool_call_need"] = False
                
            elif self.chat_type == "chat":
                if self.stream :
                    # 응답 메세지 출력
                    is_collecting_function_args = False
                    tool_calls = []
                    texts_join = ""
                    for event in run:
                        if not event.choices :
                            break
                        else :
                            last_event = event

                        delta = event.choices[0].delta
                        finish_reason = event.choices[0].finish_reason
                        if delta.content:
                            text = delta.content
                            texts_join += text
                            result_container["texts"].append(text)

                        if delta.tool_calls:
                            is_collecting_function_args = True
                            tool_call = delta.tool_calls[0]
                            if tool_call.id :
                                tool_call_target = tool_call
                            if tool_call.function.arguments:
                                tool_call_target.function.arguments += tool_call.function.arguments
                                
                        if finish_reason == "tool_calls" and is_collecting_function_args:
                            tool_calls.append(tool_call_target)
                            is_collecting_function_args = False

                    self.chat_kwargs["messages"].append({
                        "role":"assistant",
                        **({"content": [{"type": "text", "text": texts_join}]} if texts_join else {}),
                        **({"tool_calls":[{"id":tool_call.id, "type":"function", "function":{"name":tool_call.function.name, "arguments":tool_call.function.arguments}} for tool_call in tool_calls]} if tool_calls else {})
                    })

                    # run
                    if tool_calls :
                        last_event.choices[0].delta.tool_calls = tool_calls
                    result_container["run"] = last_event

                    # tool_call_need
                    if tool_calls :
                        result_container["tool_call_need"] = True
                    else :
                        result_container["tool_call_need"] = False
                    
                else :
                    self.chat_kwargs["messages"].append(run.choices[0].message.dict())
                    # 응답 메세지 출력
                    message_content = run.choices[0].message.content
                    if message_content :
                        result_container["texts"].append(message_content)

                    # run
                    result_container["run"] = run

                    # tool_call_need
                    if run.choices[0].message.tool_calls :
                        result_container["tool_call_need"] = True
                    else :
                        result_container["tool_call_need"] = False

            if self.response :
                self.response_list.append(result_container["run"])
            result_container["done"] = True
            return result_container

    def submit_tool_outputs(self, run, async_=True):
        if self.chat_type == "assistant":
            tool_outputs = []
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            for tool in tool_calls:
                tool_function = getattr(self.function_module, tool.function.name)
                tool_kwargs = json.loads(tool.function.arguments)
                output = tool_function(**tool_kwargs)
                tool_outputs.append({"tool_call_id": tool.id, "output":str(output)})
                print(f"- tool.function.name: {tool.function.name}")
                print(f"- tool_kwargs: {tool_kwargs}")
                print(f"- output: {output}")

            if self.stream :
                run = self.client.beta.threads.runs.submit_tool_outputs(
                    tool_outputs=tool_outputs,
                    thread_id=self.thread_kwargs["thread_id"],
                    run_id=run.id,
                    stream=True
                )
            else :
                run = self.client.beta.threads.runs.submit_tool_outputs_and_poll(
                    tool_outputs=tool_outputs,
                    thread_id=self.thread_kwargs["thread_id"],
                    run_id=run.id
                )

        elif self.chat_type == "chat":
            tool_calls = run.choices[0].delta.tool_calls if self.stream else run.choices[0].message.tool_calls 
            self.tool_calls = tool_calls
            for tool in tool_calls:
                tool_function = getattr(self.function_module, tool.function.name)
                tool_kwargs = json.loads(tool.function.arguments)
                output = tool_function(**tool_kwargs)
                self.chat_kwargs["messages"].append({
                    "role": "tool",
                    "tool_call_id": tool.id,
                    "content": [{"type": "text", "text": str(output)}],
                })
                print(f"- tool.function.name: {tool.function.name}")
                print(f"- tool_kwargs: {tool_kwargs}")
                print(f"- output: {output}")
            run = self.client.chat.completions.create(
                **self.chat_kwargs
            )

        result_container = self.run_control(run, async_=async_)
        return result_container
    
    def create(self, additional_messages, async_=True):
        if self.chat_type == "assistant":
            create = self.client.beta.threads.runs.create if self.stream else self.client.beta.threads.runs.create_and_poll
            run = create(
                additional_messages=additional_messages, 
                **self.thread_kwargs
            )

        elif self.chat_type == "chat":
            self.chat_kwargs["messages"] += additional_messages
            run = self.client.chat.completions.create(
                **self.chat_kwargs
            )
        
        result_container = self.run_control(run, async_=async_)
        return result_container

    def add_messages(self, messages):
        if self.chat_type == "assistant":
            # 병렬 요청이라 순서가 뒤바뀔 수 있음
            with ThreadPoolExecutor(max_workers=chat_hp.message_create_workers) as executor:
                futures = [
                    executor.submit(
                        self.client.beta.threads.messages.create,  # Keep this function unchanged
                        thread_id=self.thread_id,
                        role=message["role"],
                        content=message["content"]
                    )
                    for message in messages
                ]  
            # 요청 처리 대기
            futures_results = [future.result() for future in futures]
        elif self.chat_type == "chat":
            self.chat_kwargs["messages"] += messages
        else :
            raise Exception(f"Invalid chat_type : {self.chat_type}")
        
    def set_assistant(self, model, additional_system_text, messages, temperature, top_p, function_module):
        ### assistant 생성 
        assistant_kwargs = {
            "name":os.path.basename(os.getcwd()),
            "model":model,
            "instructions":chat_hp.system_text+"/n"+additional_system_text,
            "temperature":temperature,
            "top_p":top_p,
            **({"tools": get_tools(function_module)} if function_module and get_tools(function_module) else {})
        }
        
        assistant_id_path = ".aicastle/chat/__aicastlecache__/assistant_id"
        try:
            with open(assistant_id_path, "r") as f:
                assistant_id = f.read().strip()
            assistant = self.client.beta.assistants.update(
                assistant_id,
                **assistant_kwargs
            )
        except :
            assistant = self.client.beta.assistants.create(
                **assistant_kwargs
            )
            os.makedirs(os.path.dirname(assistant_id_path), exist_ok=True)
            with open(assistant_id_path, "w") as f:
                f.write(assistant.id)
        
        ### thread 생성
        thread = self.client.beta.threads.create(
            messages = messages[:chat_hp.max_thread_create_len] # 최대 32개 까지 밖에 안됨.....
        )
        self.thread_id = thread.id

        # 남은 메세지 추가
        self.add_messages(messages[chat_hp.max_thread_create_len:])

        self.thread_kwargs = {
            "thread_id":thread.id,
            "assistant_id":assistant.id,
            **({"stream": True} if self.stream else {})
        }

    def set_chat(self, model, additional_system_text, messages, temperature, top_p, stream, function_module):
        self.chat_kwargs = {
            "model":model,
            "temperature":temperature,
            "top_p":top_p,
            "stream":stream,
            **({"stream_options":{"include_usage":True}} if stream else {}),
            "parallel_tool_calls":False,   # tool call 이 한번에 담겨옴 
            "messages": [
                {"role":"system", "content":[{"type":"text", "text":chat_hp.system_text+"/n"+additional_system_text}]},
            ] + messages,
            **({"tools": get_tools(function_module)} if function_module and get_tools(function_module) else {})
        }
