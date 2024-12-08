import numpy as np

class AdaptivePowerNeuron:
    """
    A perceptron that adjusts its polynomial feature power and input index dynamically.
    It uses polynomial features and adjusts weights and biases based on the error.
    """
    def __init__(self, input_dim, max_power=3, learning_rate=0.001, indexing_rate=1):
        self.input_dim = input_dim
        self.max_power = max_power
        self.learning_rate = learning_rate
        self.indexing_rate = indexing_rate
        self.weights = np.random.randn(input_dim * max_power)
        self.bias = np.random.randn()
        self.current_power = 1
        self.current_index_offset = 0  # Index offset (can be fractional)
        self.index_bias = np.random.randn()  # Additional index bias

    def polynomial_features(self, x, power):
        return np.hstack([x**p for p in range(1, power + 1)])

    def interpolate_input(self, x):
        idx_adjusted = x + self.current_index_offset + self.index_bias
        return idx_adjusted

    def predict(self, x):
        x_adjusted = self.interpolate_input(x)
        poly_x = self.polynomial_features(x_adjusted, self.current_power)
        linear_output = np.dot(poly_x, self.weights[:len(poly_x)]) + self.bias
        return 1 if linear_output >= 0 else 0

    def update_weights(self, x, y):
        best_power = self.current_power
        best_index_offset = self.current_index_offset
        min_loss = float('inf')

        for power in range(1, self.max_power + 1):
            for offset in [-self.indexing_rate, 0, self.indexing_rate]:
                temp_index_offset = self.current_index_offset + offset
                x_adjusted = x + temp_index_offset + self.index_bias
                poly_x = self.polynomial_features(x_adjusted, power)
                prediction = 1 if np.dot(poly_x, self.weights[:len(poly_x)]) + self.bias >= 0 else 0
                error = y - prediction
                loss = error ** 2

                if loss < min_loss:
                    min_loss = loss
                    best_power = power
                    best_index_offset = temp_index_offset

        self.current_power = best_power
        self.current_index_offset = best_index_offset

        x_adjusted = x + self.current_index_offset + self.index_bias
        poly_x = self.polynomial_features(x_adjusted, self.current_power)
        prediction = self.predict(x)
        error = y - prediction

        self.weights[:len(poly_x)] += self.learning_rate * error * poly_x
        self.bias += self.learning_rate * error
        self.index_bias += self.learning_rate * error * 1  # Adjust index_bias dynamically
