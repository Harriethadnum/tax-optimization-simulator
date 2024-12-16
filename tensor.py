import numpy as np

class Tensor:
    def __init__(self, data):
        # Ensure the input is a numpy array
        self.data = np.array(data)
    
    def __repr__(self):
        return f"Tensor({self.data})"
    
    def shape(self):
        return self.data.shape
    
    def numpy(self):
        return self.data
    
    def add(self, other):
        return Tensor(self.data + other.data)
    
    def matmul(self, other):
        return Tensor(np.matmul(self.data, other.data))
