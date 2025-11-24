import threading
import logging
from collections import deque
from typing import Optional

logger = logging.getLogger(__name__)

class BoundedBuffer:
    def __init__(self, capacity: int = 10):
        if capacity <= 0:
            raise ValueError("Buffer capacity must be positive")
        
        self.capacity = capacity
        self.queue = deque(maxlen=capacity)
        self.mutex = threading.Lock()
        self.empty = threading.Semaphore(capacity)
        self.full = threading.Semaphore(0)
        self.operation_timeout = 5  # seconds
        
        logger.info(f"Initialized bounded buffer with capacity {capacity}")

    def insert(self, item: int, timeout: Optional[float] = None) -> bool:
        """Insert item into buffer with optional timeout"""
        timeout = timeout or self.operation_timeout
        
        try:
            if not self.empty.acquire(timeout=timeout):
                logger.warning("Timeout while waiting to insert into buffer")
                return False
                
            with self.mutex:
                self.queue.append(item)
                logger.debug(f"Inserted item {item}, buffer size: {len(self.queue)}")
                
            self.full.release()
            return True
            
        except Exception as e:
            logger.error(f"Error inserting item {item}: {e}")
            # Ensure semaphore consistency
            try:
                self.empty.release()
            except:
                pass
            return False

    def remove(self, timeout: Optional[float] = None) -> Optional[int]:
        """Remove item from buffer with optional timeout"""
        timeout = timeout or self.operation_timeout
        
        try:
            if not self.full.acquire(timeout=timeout):
                logger.warning("Timeout while waiting to remove from buffer")
                return None
                
            with self.mutex:
                item = self.queue.popleft()
                logger.debug(f"Removed item {item}, buffer size: {len(self.queue)}")
                
            self.empty.release()
            return item
            
        except Exception as e:
            logger.error(f"Error removing item: {e}")
            # Ensure semaphore consistency
            try:
                self.full.release()
            except:
                pass
            return None

    def get_size(self) -> int:
        """Get current buffer size"""
        with self.mutex:
            return len(self.queue)

    def is_empty(self) -> bool:
        """Check if buffer is empty"""
        with self.mutex:
            return len(self.queue) == 0

    def is_full(self) -> bool:
        """Check if buffer is full"""
        with self.mutex:
            return len(self.queue) == self.capacity

if __name__ == "__main__":
    # Test the buffer
    import time
    buffer = BoundedBuffer(3)
    
    print("Testing buffer operations...")
    buffer.insert(1)
    buffer.insert(2)
    buffer.insert(3)
    print(f"Buffer full: {buffer.is_full()}")
    print(f"Removed: {buffer.remove()}")
    print(f"Buffer size: {buffer.get_size()}")