import signal
import time
from functools import wraps
import eventlet


def time_limit(set_time, callback):
    def decorated(func):
        # 收到信号SIGALRM后的回调函数，参数1是信号的数字，参数2是the interrupted stack frame.
        def handler(signum, frame):
            raise RuntimeError()

        @wraps(func)
        def deco(*args, **kwargs):
            try:
                signal.signal(2, handler)
                # signal.signal(signal.SIG_IGN, handler)
                signal.alarm(set_time)
                res = func(*args, **kwargs)
                signal.alarm(0)
                return res
            except RuntimeError as e:
                callback()  # 如果不想要超时跳转，那么直接删除callback()和对应的参数
                print(e)

        return deco

    return decorated


def after_timeout():  # 超时后的处理函数
    print("Time out!")
    return


@time_limit(2, after_timeout)  # 限时 2 秒超时
def connect():  # 要执行的函数
    a = 1
    b = 2
    time.sleep(3)  # 函数执行时间，写大于2的值，可测试超时
    print('finish')
    return a, b


if __name__ == '__main__':
    # print("test")  # 此句正常执行输出
    # # if time_limit() != None  ##如果超时，此步a为None，否则为
    # a, b = connect()
    # print(a)  # 正常输出
    # print(b)  # 正常输出
    # c = 4
    # print(c)  # 此步正常输出

    eventlet.monkey_patch()  # 必须加这条代码
    with eventlet.Timeout(1, False):  # 设置超时时间为2秒
        print('run')
        time.sleep(10)
        print('skip')
    print('end')
