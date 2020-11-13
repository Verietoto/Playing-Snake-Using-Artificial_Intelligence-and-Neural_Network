from Parameters import *
from numba import jit

class NeuralNetwork():
    def __init__(self, networkShape):
        self.shape = networkShape

    def feedForward(self, input, weight, biases):
        self.weights = weight
        self.biasses = biases

        input = np.array(input).reshape(-1)

        FF = copy.deepcopy(input)

        #Feed Forward
        for i in range(len(self.weights)):
            FF = (np.dot(FF, self.weights[i]) + self.biasses[i])
        return FF

    def createBiasses(self):
        biasses = []
        for i in range(len(self.shape)-1):
            bias = np.random.uniform(-1,1,self.shape[i+1])
            biasses.append(bias)
        return np.array(biasses)

    def createWeight(self):
        weights = []
        for i in range(len(self.shape)-1):
            weight = np.random.uniform(-1,1,(self.shape[i], self.shape[i+1]))
            weights.append(weight)
        return np.array(weights)

@jit(nopython=True)
def sigmoid(data):
     return 1/(1+np.exp(-data))

@jit(nopython=True)
def relu(FF):
    return  np.maximum(0,FF)


