# adaptive_power_model.py
from dense_layer import DenseLayer

class AdaptivePowerModel:
    def __init__(self):
        self.layers = []

    def add(self, layer):
        self.layers.append(layer)

    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def train(self, x, y, epochs, batch_size):
        num_samples = x.shape[0]
        for epoch in range(epochs):
            total_loss = 0
            for i in range(0, num_samples, batch_size):
                x_batch = x[i : i + batch_size]
                y_batch = y[i : i + batch_size]
                # Forward pass
                predictions = self.forward(x_batch)
                # Backward pass
                for layer in reversed(self.layers):
                    total_loss += layer.backward(x_batch, y_batch)
            print(f"Epoch {epoch + 1}, Loss: {total_loss / (num_samples / batch_size):.4f}")
