from pandas import np


class Network:
    weightMatrixList = []
    bias = 1

    def __init__(self, layers: []):
        self.weightMatrixList = []
        for layerLevel in range(1, len(layers)):
            self.weightMatrixList.append(np.random.rand(layers[layerLevel - 1] + self.bias, layers[layerLevel]))
        self.weightMatrixList = np.array(self.weightMatrixList)

    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))

    def calc(self, inputValues: [], ind):
        res = np.append(np.array(inputValues), self.bias)
        for weights in self.weightMatrixList:

            res = np.matmul(res, weights)
            res = self.sigmoid(res)
            res = np.append(res, self.bias)
        if ind == 1:
            print(str(inputValues)+ "\n=>" +str(res))
        return res[0:-1]

    def getWeightsAsList(self):

        flatten = np.array([])
        for matrix in self.weightMatrixList:
            flatten = np.append(flatten, matrix.flatten())

        return np.array(flatten)


    def setWeightsAsList(self, wList:np.array):
        indexx = 0
        for oldMatrix in self.weightMatrixList:

            size = oldMatrix.shape[0] * oldMatrix.shape[1]
            listOfMatrix = wList[indexx:size+indexx]
            indexx += size
            #("reshape: " + str(listOfMatrix) + "\n from " + str(len(listOfMatrix))+ "\n to " + str(oldMatrix.shape))
            oldMatrix = np.reshape(listOfMatrix, oldMatrix.shape)