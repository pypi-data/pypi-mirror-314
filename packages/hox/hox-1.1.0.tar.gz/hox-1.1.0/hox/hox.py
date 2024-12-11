import numpy as np
import pickle
from tqdm import tqdm

class Sigmoid():
    def forward(self, x):
        return np.divide(np.float32(1), (np.float32(1) + np.exp(-x)))
    def backward(self, layer_output, delta):
        return np.multiply(delta, np.multiply(layer_output, (np.float32(1) - layer_output)))
    def initialize(self, neurons, input_neurons):
        return np.random.uniform(low=-0.1, high=0.1, size=(neurons, input_neurons)).astype(np.float32)

class Relu():
    def forward(self, x):
        return np.maximum(x, np.float32(0))
    def backward(self, layer_output, delta):
        return np.multiply(delta, (layer_output > np.float32(0)))
    def initialize(self, neurons, input_neurons):
        return np.random.normal(loc=0, scale=np.sqrt(2 / input_neurons), size=(neurons, input_neurons)).astype(np.float32)

class Layer():
    def __init__(self, input_neurons, neurons, activation):
        self.activation = activation
        self.weights = activation.initialize(neurons, input_neurons)
        self.biases = np.zeros(neurons, dtype=np.float32)

    def forward(self, x):
        self.input, self.output = x, self.activation.forward(np.dot(self.weights, x) + self.biases)
        return self.output

    def backward(self, delta):
        delta = self.activation.backward(self.output, delta)
        self.grad_weights += np.outer(delta, self.input)
        self.grad_biases += delta
        return np.dot(self.weights.T, delta)

    def zero_grad(self):
        self.grad_weights, self.grad_biases = np.zeros_like(self.weights), np.zeros_like(self.biases)

class Model():
    def __init__(self, layers):
        self.layers, self.backward_passes = layers, 0
        for layer in self.layers: layer.zero_grad()

    @classmethod
    def create(cls, layers):
        return cls(layers)

    @classmethod
    def load(cls, name):
        with open(name + ".pkl", "rb") as file:
            layers = pickle.load(file)
        return cls(layers)

    def save(self, name):
        with open(name + ".pkl", "wb") as file:
            pickle.dump(self.layers, file)

    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def backward(self, y):
        delta = self.layers[-1].output - y
        for layer in reversed(self.layers):
            delta = layer.backward(delta)
        self.backward_passes += 1

    def update_weights(self, lr):
        factor = np.float32(lr / self.backward_passes)
        for layer in self.layers:
            layer.weights -= layer.grad_weights * factor
            layer.biases -= layer.grad_biases * factor
            layer.zero_grad()
        self.backward_passes = 0

    def train(self, X, Y, **options):
        rate, batch_size, epochs = options.get("rate", 0.5), options.get("batch_size", 16), options.get("epochs", 1)
        data_len, loss_format = len(Y), lambda l: f"{l:.4f}"
        for epoch in range(epochs):
            pbar = tqdm(range(0, len(X), batch_size), desc=f"Epoch {epoch}", bar_format='{l_bar}{bar}|[{elapsed}<{remaining}]{postfix}')
            loss, loss_counter = 0, 0
            for batch_start in pbar:
                for index in range(batch_start, min(batch_start + batch_size, len(X))):
                    output = self.forward(X[index])
                    if index % (data_len / 50) == 0:
                        loss_counter += 1
                        loss += abs(np.mean(Y[index] - output))
                        pbar.set_postfix(loss=loss_format(loss / loss_counter))
                    self.backward(Y[index])
                self.update_weights(rate)
        print("Training completed.")
