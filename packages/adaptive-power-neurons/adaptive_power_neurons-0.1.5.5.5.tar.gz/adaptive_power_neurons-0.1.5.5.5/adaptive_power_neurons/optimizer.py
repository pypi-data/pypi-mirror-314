# optimizer.py

class Optimizer:
    """
    Base class for optimizers.
    """
    def update(self, params, grads):
        """
        Updates parameters based on gradients.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")


class SGD(Optimizer):
    """
    Stochastic Gradient Descent optimizer.
    """
    def __init__(self, learning_rate):
        self.learning_rate = learning_rate

    def update(self, params, grads):
        for param, grad in zip(params, grads):
            param -= self.learning_rate * grad
