import multiprocessing


def 多进程_创建进程锁():
    """
    创建并返回一个新的进程锁对象。

    返回：
        - 进程锁对象，如果创建成功
        - None，如果创建失败

    示例：
    进程锁对象 = 多进程_创建进程锁()
     with 进程锁对象:
            # 执行需要加锁的代码块
            print("此代码块受锁保护")
    """
    try:
        lock = multiprocessing.Lock()
        return lock
    except Exception:
        return None