from adaptive_power_neuron import AdaptivePowerNeuron
import numpy as np

class AdaptivePowerNeurons:
    """
    Neural Network composed of adaptive power neurons.

    This class implements a multi-layer neural network using adaptive power neurons.
    
    Attributes:
        layers (list): A list of layers, each containing adaptive power neurons.
        optimizer (Optimizer): Optimizer for updating the weights of the network.
    """
    
    def __init__(self):
        """
        Initializes the Adaptive Power Neurons model.
        """
        self.layers = []

    def add_layer(self, num_perceptrons, input_dim, max_power, learning_rate, indexing_rate):
        """
        Adds a new layer of adaptive power neurons to the model.

        Args:
            num_perceptrons (int): The number of perceptrons (neurons) in the layer.
            input_dim (int): The number of input features to each neuron.
            max_power (int): Maximum power for the adaptive neuron.
            learning_rate (float): Learning rate for the neuron.
            indexing_rate (float): Indexing rate for the neuron.
        """
        for _ in range(num_perceptrons):
            # Add each perceptron (neuron) to the layer
            layer = AdaptivePowerNeuron(input_dim, max_power, learning_rate, indexing_rate)
            self.layers.append(layer)

    def set_optimizer(self, optimizer):
        """
        Sets the optimizer for the entire network.

        Args:
            optimizer (Optimizer): Optimizer used to update weights during training.
        """
        self.optimizer = optimizer

    def fit(self, X, y, epochs):
        """
        Trains the model over a number of epochs.

        Args:
            X (numpy.ndarray): Input data for training.
            y (numpy.ndarray): Target output for training.
            epochs (int): Number of training epochs.
        """
        for epoch in range(epochs):
            total_loss = 0
            for x, target in zip(X, y):
                for layer in self.layers:
                    layer.update_weights(x, target)
                    total_loss += np.sum((layer.predict(x) - target) ** 2)  # Loss calculation
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss / len(X)}")

    def predict(self, X):
        """
        Makes predictions using the trained model.

        Args:
            X (numpy.ndarray): Input data for prediction.

        Returns:
            numpy.ndarray: Predicted output for each input sample.
        """
        predictions = []
        for x in X:
            prediction = np.zeros(len(self.layers))  # Placeholder for the output of each layer
            for idx, layer in enumerate(self.layers):
                prediction[idx] = layer.predict(x)  # Get predictions from each layer
            predictions.append(prediction)
        return np.array(predictions)
