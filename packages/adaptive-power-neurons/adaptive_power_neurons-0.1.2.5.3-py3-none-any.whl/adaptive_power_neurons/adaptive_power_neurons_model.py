import numpy as np
from .adaptive_power_neurons import AdaptivePowerNeuron

class AdaptivePowerNeurons:
    """
    A neural network model using layers of AdaptivePowerNeurons.
    This model can have multiple layers of perceptrons, and the optimizer can be used to adjust
    hyperparameters dynamically.
    """
    def __init__(self):
        self.layers = []
        self.optimizer = None

    def add_layer(self, num_perceptrons, input_dim, max_power, learning_rate, indexing_rate):
        layer = [
            AdaptivePowerNeuron(input_dim, max_power, learning_rate, indexing_rate)
            for _ in range(num_perceptrons)
        ]
        self.layers.append({'perceptrons': layer, 'learning_rate': learning_rate, 'max_power': max_power, 'indexing_rate': indexing_rate})

    def set_optimizer(self, optimizer):
        self.optimizer = optimizer
        for layer in self.layers:
            layer_avg_params = {
                'learning_rate': np.mean([p.learning_rate for p in layer['perceptrons']]),
                'max_power': np.mean([p.max_power for p in layer['perceptrons']]),
                'indexing_rate': np.mean([p.indexing_rate for p in layer['perceptrons']])
            }
            for perceptron in layer['perceptrons']:
                self.optimizer.apply_optimizer(perceptron, layer_avg_params)

    def predict(self, X):
        for layer in self.layers:
            new_X = []
            for xi in X:
                layer_output = [perceptron.predict(xi) for perceptron in layer['perceptrons']]
                new_X.append(layer_output)
            X = np.array(new_X)
        return X

    def fit(self, X, y, epochs=10):
        for epoch in range(epochs):
            for layer in self.layers:
                for perceptron in layer['perceptrons']:
                    for xi, yi in zip(X, y):
                        perceptron.update_weights(xi, yi)
            loss = self.calculate_loss(X, y)
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss}")

    def calculate_loss(self, X, y):
        total_loss = 0
        for xi, yi in zip(X, y):
            prediction = self.predict([xi])
            total_loss += (yi - prediction[0][0]) ** 2
        return total_loss / len(y)
