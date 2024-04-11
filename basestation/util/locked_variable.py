from threading import Lock

class LockedVariable:
    def __init__(self, value, default_value):
        self.variable = value
        self.lock = Lock()
        self.default_value = default_value
    
    @property
    def variable(self):
        return self._variable
    
    @variable.setter
    def variable(self, value):
        self._variable = value
    
    def set_with_lock(self, blocking: bool, value, timeout=1):
        if blocking:
            acquired = self.lock.acquire(blocking=blocking, timeout=timeout)
        else:
            acquired = self.lock.acquire(blocking=blocking)

        if acquired:
            self.variable = value
            self.lock.release()
    
    def get_with_lock(self, blocking: bool, timeout=1):
        if blocking:
            acquired = self.lock.acquire(blocking=blocking, timeout=timeout)
        else:
            acquired = self.lock.acquire(blocking=blocking)
        
        if acquired:
            value = self.variable
            self.lock.release()
            return value
        else:
            return self.default_value