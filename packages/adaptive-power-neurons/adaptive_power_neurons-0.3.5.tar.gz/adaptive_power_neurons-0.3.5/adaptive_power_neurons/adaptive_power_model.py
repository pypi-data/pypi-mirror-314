from .dense_layer import DenseLayer
from .activation import Activation 

class AdaptivePowerModel:
    def __init__(self):
        self.layers = []

    def add(self, layer):
        """
        Add a layer to the model.
        """
        self.layers.append(layer)

    def forward(self, x):
        """
        Perform a forward pass through all layers.
        """
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def train(self, x, y, epochs, batch_size):
        """
        Train the model using forward and backward passes.
        """
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

    def predict(self, x):
        """
        Predict the output for a given input x.
        Perform a forward pass and return the predicted values.
        """
        return self.forward(x)
