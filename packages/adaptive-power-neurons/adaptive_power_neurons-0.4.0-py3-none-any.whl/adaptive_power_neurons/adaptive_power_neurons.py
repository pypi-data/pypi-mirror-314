# adaptive_power_neuron.py
import numpy as np
from .activation import Activation

class AdaptivePowerNeuron:
    def __init__(self, input_dim, max_power, optimizer, indexing_rate):
        self.input_dim = input_dim
        self.max_power = max_power
        self.optimizer = optimizer  # Use optimizer for updates
        self.indexing_rate = indexing_rate
        self.current_index_offset = 0
        self.weights = np.random.randn(input_dim) * 0.1  # Small random weights
        self.bias = 0

    def predict(self, x):
        x_transformed = np.power(x, self.max_power + self.current_index_offset)
        return np.dot(x_transformed, self.weights) + self.bias

    def update(self, x, y):
        batch_size = x.shape[0]

        # Predictions
        predictions = self.predict(x)

        # Gradients for weights, bias, and index offset
        x_transformed = np.power(x, self.max_power + self.current_index_offset)
        grad_weights = (2 / batch_size) * np.dot(x_transformed.T, (predictions - y))
        grad_bias = (2 / batch_size) * np.sum(predictions - y)
        grad_index_offset = np.mean((predictions - y) * np.sum(x_transformed * np.log(x + 1e-10), axis=1))

        # Update parameters using the optimizer
        self.optimizer.update(
            params=[self.weights, self.bias],
            grads=[grad_weights, grad_bias]
        )

        # Update index offset directly
        self.current_index_offset -= self.indexing_rate * grad_index_offset

        # Loss
        loss = np.mean((predictions - y) ** 2)
        return loss
