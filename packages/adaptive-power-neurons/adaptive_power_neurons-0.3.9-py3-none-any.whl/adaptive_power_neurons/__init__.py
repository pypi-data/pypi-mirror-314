# Defining __all__ to specify the public interface of this package
__all__ = [
    'Activation',            # Activation class for activation functions
    'SGD',                   # Stochastic Gradient Descent optimizer
    'Optimizer',             # Optimizer class for general optimization tasks
    'AdaptivePowerNeuron',   # Adaptive Power Neuron class
    'DenseLayer',            # Dense Layer class (ensure this file exists)
    'AdaptivePowerModel'     # Adaptive Power Model class
]

# Importing necessary classes from the respective modules
from .activation import Activation  # Class for activation functions
from .optimizer import SGD, Optimizer  # Stochastic Gradient Descent and Optimizer classes
from .adaptive_power_neurons import AdaptivePowerNeuron  # Adaptive Power Neuron class
from .dense_layer import DenseLayer  # DenseLayer class (ensure this file exists)
from .adaptive_power_model import AdaptivePowerModel  # Adaptive Power Model class
