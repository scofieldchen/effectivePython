import time
from typing import Any, Dict, Optional

import requests
from requests.exceptions import ConnectionError, Timeout
from requests.models import Response


def retry_request(url: str,
                  params: Optional[Dict[str, Any]] = None,
                  headers: Optional[Dict[str, Any]] = None,
                  proxies: Optional[Dict[str, Any]] = None,
                  timeout: int = 5,
                  total_tries: int = 5,
                  initial_wait: float = 0.5,
                  backoff_factor: float = 2.0,
                  **kwargs) -> Response:
    """装饰requests.get, 实现重试策略，采用指数退避算法，
    所有重试失败后主动引发异常
    
    Args:
        url(str): 请求URL
        params(dict): 请求参数
        headers(dict): 自定义请求头
        proxies(dict): 代理IP
        timeout(int): 请求超时，秒
        total_tries(int): 总尝试次数
        initial_wait(float): 第一次请求失败后的等待时间，秒
        backoff_factor(float): 指数因子，重试策略采用指数退避算法，
            delay = initial_wait * backoff_factor ^ (total_tries - 1)
            核心原理是每次失败后等待更长的时间再进行重试
    
    Returns:
        requests.Response
    """
    delay = initial_wait
    for _ in range(1, total_tries + 1):
        try:
            resp = requests.get(url, params, headers=headers,
                                proxies=proxies, timeout=timeout)
            resp.raise_for_status()
            return resp
        except (ConnectionError, Timeout):
            time.sleep(delay)
            delay *= backoff_factor
    
    raise Exception(f"Request failed, total tries = {total_tries}")
