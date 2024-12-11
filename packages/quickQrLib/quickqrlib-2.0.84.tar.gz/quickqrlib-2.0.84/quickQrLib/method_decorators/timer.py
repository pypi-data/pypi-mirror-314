import time
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(self,  *args, **kwargs):
        start_time = time.time()
        result = func(self, *args, **kwargs)
        end_time = time.time()
        total_sec = end_time - start_time
               
        if self.__class__ is not None:
            class_name = self.__class__.__name__
            method_name = func.__name__
            print("============================================================")
            print(f"Class: {class_name}, Method: {method_name} method exeucted in {round(total_sec, 2)} seconds")
            print("============================================================")
        else:
            method_name = func.__name__
            print("============================================================")
            print(f"{func.__name__} method exeucted in {round(total_sec, 2)} seconds")
            print("============================================================")            
        return result
    return wrapper
