# dense_layer.py
import numpy as np
from adaptive_power_neurons import AdaptivePowerNeuron
from activation import Activation

class DenseLayer:
    def __init__(self, input_dim, output_dim, max_power, optimizer, indexing_rate, activation="identity"):
        self.neurons = [
            AdaptivePowerNeuron(input_dim, max_power, optimizer, indexing_rate)
            for _ in range(output_dim)
        ]
        self.activation = getattr(Activation, activation)  # Activation function
        self.activation_derivative = getattr(Activation, f"{activation}_derivative")  # Derivative of activation

    def forward(self, x):
        self.input = x  # Store input for backpropagation
        self.output = np.array([neuron.predict(x) for neuron in self.neurons]).T
        self.activated_output = self.activation(self.output)  # Apply activation
        return self.activated_output

    def backward(self, x, y):
        # Calculate gradients with respect to activation function
        grad_loss_activation = (self.activated_output - y) * self.activation_derivative(self.output)
        losses = []
        for i, neuron in enumerate(self.neurons):
            # Use the gradient of the activation function in backpropagation
            loss = neuron.update(self.input, grad_loss_activation[:, i])
            losses.append(loss)
        return np.mean(losses)
