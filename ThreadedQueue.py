import threading

class ThreadedQueue:
    
    def __init__(self):
        self.queue = []
        self.empty = threading.Semaphore(25)
        self.full = threading.Semaphore(0)
        self.lock = threading.Lock()
        
    def put(self,item):
        self.empty.acquire()
        self.lock.acquire()
        self.queue.append(item)
        self.lock.release()
        self.full.release()
    
    def get(self):
        self.full.acquire()
        self.lock.acquire()
        artifact = self.queue.pop(0)
        self.lock.release()
        self.empty.release()
        return artifact
