# 一些额外可能用到的功能集合
import time

# Retrying context manager
class Retry(object):
    
    """
    一个对某段程序可以进行重试的封装方法
    
    e.g.
    
    for retry in Retry(max_tries=5):
        with retry:
            # 可能出错
            do_something()
    
    if retry.isSuccess:
        print("执行成功")
    else:
        print("执行失败")
    
    """
    
    def __init__(self, max_tries=5, wait_time=5):
        self.max_tries = max_tries
        self.wait_time = wait_time
        
    def __iter__(self):
        for i in range(self.max_tries):
            yield self
            if self.isSuccess or i == self.max_tries - 1:
                return 
            time.sleep(self.wait_time)
            
    def __enter__(self):
        self.isSuccess = False
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.isSuccess = True
        else:
            print(exc_val)
        return True