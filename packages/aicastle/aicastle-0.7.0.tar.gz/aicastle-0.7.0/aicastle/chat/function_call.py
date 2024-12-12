def execute_python_code(code: str) -> dict:
    """
    사용자 시스템에서 실행 할 Python 코드를 작성하세요. (코드 내에 절대로 def 는 사용하면 안됩니다.)
    이 함수는 사용자 시스템에서 실행되며, 사용자의 파일 읽기, 수정 및 시스템을 제어할 수 있습니다.
    사용자에게 파일 업로드를 요청하지 말고 이 함수로 사용자 파일에 접근하여 code_interpreter 처럼 사용하세요.
    이전에 실행된 코드의 결과는 전역 세션 변수(global_session)에 저장되므로 지속적인 확인 및 참조가 가능합니다.
    사용자의 요청이 단계적 수행이 필요한 경우 단계적으로 function을 요청 하십시오.
    """

    global global_session
    if "global_session" not in globals():
        global_session = {
            "global_scope": {},
            "local_scope": {}
        }

    try:
        exec(code, global_session["global_scope"], global_session["local_scope"])
        result = {
            "success": True,
            "result": global_session["local_scope"].get("operation_result", None)
        }
    except Exception as e:
        result = {
            "success": False,
            "error": str(e)
        }
    
    return str(result)
