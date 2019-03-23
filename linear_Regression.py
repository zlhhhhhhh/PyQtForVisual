import numpy as np


# learningRate学习率，Loopnum迭代次数
class linear_Regression(object):
    def __init__(self,data_x,data_y,learningRate=0.001,Loopnum=5000):
        self.data_x = data_x
        self.data_y = data_y
        self.learningRate = learningRate
        self.Loopnum = Loopnum

    def linear_Regression(self):
        Weight = np.ones(shape=(1, self.data_x.shape[1]))
        baise = np.array([[1]])

        for num in range(self.Loopnum):
            WXPlusB = np.dot(self.data_x, Weight.T) + baise

            loss = np.dot((self.data_y - WXPlusB).T, self.data_y - WXPlusB) / self.data_y.shape[0]
            w_gradient = -(2 / self.data_x.shape[0]) * np.dot((self.data_y - WXPlusB).T, self.data_x)
            baise_gradient = -2 * np.dot((self.data_y - WXPlusB).T, np.ones(shape=[self.data_x.shape[0], 1])) / self.data_x.shape[0]

            Weight = Weight - self.learningRate * w_gradient
            baise = baise - self.learningRate * baise_gradient
            #if num % 50 == 0:
            #    print(loss)  # 每迭代50次输出一次loss
        return (Weight, baise)

if __name__ =="__main__":
    data_x = np.random.normal(0, 10, [5, 3])
    Weights = np.array([[3, 4, 6]])
    data_y = np.dot(data_x, Weights.T) + 5

    print(data_x,data_y)
    print(type(data_x),type(data_y))
    rl = linear_Regression(data_x, data_y, learningRate=0.001, Loopnum=5000)
    res = rl.linear_Regression()
    print(res[0], res[1])

