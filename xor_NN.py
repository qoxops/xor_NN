import numpy as np

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def dsigmoid(x):
    return (x) * (1.0 - (x))

class NN:
    def __init__(self, num_input, num_hidden, num_output):
        #入力層から隠れ層への重み行列
        #np.random.uniform -> 一様乱数
        self.W1 = np.random.uniform(-1.0, 1.0, (num_input, num_hidden))
        self.hidden_bias = np.ones(num_hidden, dtype = float)
        #隠れ層から出力層への重み行列
        self.W2 = np.random.uniform(-1.0, 1.0, (num_hidden, num_output))
        self.output_bias = np.ones(num_output, dtype = float)

    def forward(self, x):
        h = sigmoid(np.dot(self.W1.T, x) + self.hidden_bias)
        return sigmoid(np.dot(self.W2.T, h) + self.output_bias)

    def cost(self, data, target):
        N = data.shape[0]
        E = 0.0
        for i in range(N):
            y, t = self.forward(data[i]), target[i]
            E += np.sum((y - t) * (y - t))
        return 0.5 * E / float(N)

    def train(self, data, target, epoches = 30000, learning_rate = 0.1, monitor_period = None):
        for epoch in range(epoches):
            # 学習データから1サンプルをランダムに選ぶ
            index = np.random.randint(0, data.shape[0])
            x, t = data[index], target[index]
            # 入力から出力まで前向きに信号を伝搬
            h = sigmoid(np.dot(self.W1.T, x) + self.hidden_bias)
            y = sigmoid(np.dot(self.W2.T, h) + self.output_bias)
            # 隠れ層->出力層の重みの修正量を計算
            output_delta = (y - t) * dsigmoid(y)
            grad_W2 = np.dot(np.atleast_2d(h).T, np.atleast_2d(output_delta))
            # 隠れ層->出力層の重みを更新
            self.W2 -= learning_rate * grad_W2
            self.output_bias -= learning_rate * output_delta
            # 入力層->隠れ層の重みの修正量を計算
            hidden_delta = np.dot(self.W2, output_delta) * dsigmoid(h)
            grad_W1 = np.dot(np.atleast_2d(x).T, np.atleast_2d(hidden_delta))
            # 入力層->隠れ層の重みを更新
            self.W1 -= learning_rate * grad_W1
            self.hidden_bias -= learning_rate * hidden_delta
            # 現在の目的関数の値を出力
            if monitor_period != None and epoch % monitor_period == 0:
                print ("Epoch:%d, Cost:%f" % (epoch, self.cost(data, target)))
        print ("Training finished.")

    def predict(self, x):
        return np.argmax(self.forward(x))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=("Specify options"))
    parser.add_argument("--epoches", dest="epoches", type=int, required=True)
    parser.add_argument("--learning_rate", dest="learning_rate", type=float, default=0.1)
    parser.add_argument("--hidden", dest="hidden", type=int, default=20)
    args = parser.parse_args()

    nn = NN(2, args.hidden, 1)

    data = np.array([[0, 0], [0 ,1], [1, 0], [1, 1]])
    target = np.array([0, 1, 1, 0])

    nn.train(data, target, args.epoches, args.learning_rate, monitor_period=1000)

    for x in data:
        print ("%s : predicted %s" % (x, nn.forward(x)))
