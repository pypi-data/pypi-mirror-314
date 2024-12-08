class Optimizer:
    """
    An optimizer class that allows the adjustment of learning rate, power, and indexing power during training.
    """
    def __init__(self, learning_rate=0.001, max_power=3, indexing_rate=0.1):
        self.learning_rate = learning_rate
        self.max_power = max_power
        self.indexing_rate = indexing_rate

    def apply_optimizer(self, perceptron, layer_avg_params):
        perceptron.learning_rate = (self.learning_rate + layer_avg_params['learning_rate']) / 2
        perceptron.max_power = (self.max_power + layer_avg_params['max_power']) / 2
        perceptron.indexing_rate = (self.indexing_rate + layer_avg_params['indexing_rate']) / 2
