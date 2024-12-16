import numpy as np
from activations import relu, sigmoid
from tensor import Tensor

class Dense:
    def __init__(self, input_size, output_size, activation=None):
        # Initialize weights and bias (random values)
        self.weights = np.random.randn(input_size, output_size) * 0.01
        self.bias = np.zeros(output_size)
        self.activation = activation

    def forward(self, x):
        # Linear transformation: X * W + b
        self.input = x
        self.output = np.dot(x.data, self.weights) + self.bias
        if self.activation:
            self.output = self.activation(self.output)
        return Tensor(self.output)
