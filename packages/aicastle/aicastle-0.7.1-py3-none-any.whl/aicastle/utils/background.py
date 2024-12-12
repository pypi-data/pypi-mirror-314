import threading
import time

########### Thread ###########
def run_thread(func, *args, _start=True, **kwargs):
    """
    주어진 함수를 백그라운드 스레드에서 실행하고, 결과를 result_container에 저장합니다.
    
    :param func: 백그라운드에서 실행할 함수
    :param kwargs: 함수에 전달할 키워드 인수
    :return: 함수 실행 결과와 상태를 담는 딕셔너리
    """
    
    result_container = {'done': False, 'result': None, 'error': None}
    
    def wrapper():
        try:
            result = func(*args, **kwargs)
            result_container['result'] = result
        except Exception as error:
            result_container['error'] = error
        finally:
            result_container['done'] = True

    # 백그라운드에서 실행할 스레드 생성
    thread = threading.Thread(target=wrapper)
    result_container['thread'] = thread
    
    # 스레드를 데몬으로 설정 (메인 프로그램 종료 시 강제 종료)
    thread.daemon = True
    
    # 스레드 시작
    if _start :
        thread.start()
    
    return result_container


def run_thread_multi(func, num_workers=100, args_list=None, kwargs_list=None, _sleep=0.05):
    """
    동일한 함수를 여러 인자로 백그라운드 스레드에서 여러 번 실행하고, 결과를 저장합니다.
    
    :param func: 백그라운드에서 실행할 함수
    :param kwargs_list: 각 호출에 사용할 키워드 인수들의 리스트
    :param sleep: 각 스레드의 상태를 확인할 대기 시간 (초)
    :return: 각 호출의 결과와 상태를 담는 딕셔너리
    """
    
    if (args_list is None) and (kwargs_list is None):
        raise Exception("Either args_list or kwargs_list must be provided.")
    elif isinstance(args_list, list) and isinstance(kwargs_list, list) :
        if not len(args_list) == len(kwargs_list):
            raise Exception("The lengths of args_list and kwargs_list must be equal.")
        if len(args_list) == 0 :
            raise Exception("The provided args_list and kwargs_list cannot be empty.")
    elif kwargs_list is None :
        if len(args_list) == 0 :
            raise Exception("The provided args_list cannot be empty.")
        else :
            kwargs_list = [{} for _ in range(len(args_list))]
    elif args_list is None :
        if len(kwargs_list) == 0 :
            raise Exception("The provided kwargs_list cannot be empty.")
        else :
            args_list = [[] for _ in range(len(kwargs_list))]
    
    result_container = {'done': False, 'result': None, 'error': None, 'done_count':0, 'done_rate':0}

    def thread_control(result, num_workers = num_workers):
        result_len = len(result)
        working_idx_list = []
        for target_idx in range(result_len):
            while True :
                for working_idx in working_idx_list:
                    working_item = result[working_idx]
                    if working_item['done'] :
                        working_idx_list.remove(working_idx)
                if len(working_idx_list) < num_workers :
                    target_item = result[target_idx]
                    target_item['thread'].start()
                    working_idx_list.append(target_idx)
                    break

    def wrapper():
        try:
            result = []
            for args, kwargs in zip(args_list, kwargs_list):
                result.append(run_thread(func, *args, _start=False, **kwargs))
            result_container['result'] = result

            run_thread(thread_control, result)
            
            while True:
                result_len = len(result)
                done_count = 0
                for a_result in result:
                    if a_result['done']:
                        done_count +=1
                        
                if done_count == result_len:
                    result_container['done'] = True
                    result_container['done_count'] = done_count
                    result_container['done_rate'] = 1
                    break
                else :
                    result_container['done_count'] = done_count
                    result_container['done_rate'] = done_count / result_len
                     
                time.sleep(_sleep)
                
        except Exception as error:
            result_container['error'] = error
        finally:
            result_container['done'] = True
   
    # 백그라운드에서 실행할 스레드 생성
    thread = threading.Thread(target=wrapper)
    result_container['thread'] = thread
        
    # 스레드를 데몬으로 설정 (메인 프로그램 종료 시 강제 종료)
    thread.daemon = True
    
    # 스레드 시작
    thread.start()
    
    return result_container


def thread_join(result_container, max_time=60, sleep=0.05):
    """
    주어진 시간 내에 백그라운드 스레드가 완료될 때까지 대기합니다.
    
    :param result_container: 스레드의 결과와 상태를 담고 있는 딕셔너리
    :param max_time: 최대 대기 시간 (초)
    :param sleep: 각 스레드의 상태를 확인할 대기 시간 (초)
    :return: 완료된 스레드의 결과와 상태를 담은 딕셔너리
    """
    
    s_time = time.time()
    while not result_container['done']:
        if time.time() - s_time > max_time:
            raise Exception(f"max_time : {max_time} sec")
        time.sleep(sleep)
    return result_container
