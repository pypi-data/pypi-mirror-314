# 이 코드는 EsterHlav의 일부 아이디어와 구현을 참고하여 작성되었습니다.
# https://github.com/EsterHlav/MLP-Numpy-Implementation-Gradient-Descent-Backpropagation
# Copyright (c) 2017 EsterHlav
# Licensed under the MIT License.
# MIT License: https://opensource.org/licenses/MIT

import numpy as np
import os

class MLPForMINIST:
    def __init__(self, input_length, hidden_length, output_length, learning_rate=0.01):
        self.input_length = input_length
        self.hidden_length = hidden_length
        self.output_length = output_length
        self.learning_rate = learning_rate

        self.W1 = np.random.randn(input_length, hidden_length) * 0.01
        self.b1 = np.zeros((1, hidden_length))
        self.W2 = np.random.randn(hidden_length, output_length) * 0.01
        self.b2 = np.zeros((1, output_length))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def softmax(self, x):
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)

    def calc_loss(self, y, y_pred):
        m = y.shape[0]
        loss = -np.sum(y * np.log(y_pred + 1e-9)) / m
        return loss

    def forward(self, X):
        Z1 = np.dot(X, self.W1) + self.b1
        A1 = self.sigmoid(Z1)  # 은닉층 출력
        Z2 = np.dot(A1, self.W2) + self.b2
        A2 = self.softmax(Z2)  # 출력층 출력
        return Z1, A1, Z2, A2  # 모든 값을 반환

    def backward(self, X, y, Z1, A1, Z2, A2):
        m = X.shape[0]

        # 출력층 기울기 계산
        dZ2 = A2 - y
        dW2 = np.dot(A1.T, dZ2) / m
        db2 = np.sum(dZ2, axis=0, keepdims=True) / m

        # 은닉층 기울기 계산
        dA1 = np.dot(dZ2, self.W2.T)
        dZ1 = dA1 * self.sigmoid_derivative(A1)
        dW1 = np.dot(X.T, dZ1) / m
        db1 = np.sum(dZ1, axis=0, keepdims=True) / m

        # 가중치 업데이트
        self.W1 -= self.learning_rate * dW1
        self.b1 -= self.learning_rate * db1
        self.W2 -= self.learning_rate * dW2
        self.b2 -= self.learning_rate * db2

    def fit(self, X_train, y_train, X_test, y_test, epoch=1000, patience=10):
        train_losses = []
        test_losses = []
        best_loss = float('inf')
        patient_count = 0
        for i in range(epoch):
            # 순전파
            Z1_train, A1_train, Z2_train, A2_train = self.forward(X_train)
            Z1_test, A1_test, Z2_test, A2_test = self.forward(X_test)

            # 손실 계산
            train_loss = self.calc_loss(y_train, A2_train)
            test_loss = self.calc_loss(y_test, A2_test)
            train_losses.append(train_loss)
            test_losses.append(test_loss)

            # 역전파
            self.backward(X_train, y_train, Z1_train, A1_train, Z2_train, A2_train)

            if i % 100 == 0:
                print(f"epoch: {i} | train_loss: {train_loss} | test_loss: {test_loss}")

            # Early stopping
            if test_loss < best_loss:
                best_loss = test_loss
                patient_count = 0
            else:
                patient_count += 1
            if patient_count > patience:
                print(f"Early stopping at epoch {i}")
                break

        return train_losses, test_losses

    def predict(self, X):
        _, _, _, A2 = self.forward(X)
        return np.argmax(A2, axis=1)
    
    def save_model(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        np.save(os.path.join(folder_path, "W1.npy"), self.W1)
        np.save(os.path.join(folder_path, "b1.npy"), self.b1)
        np.save(os.path.join(folder_path, "W2.npy"), self.W2)
        np.save(os.path.join(folder_path, "b2.npy"), self.b2)
        print(f"Model saved to {folder_path}")

    def load_model(self, folder_path):
        self.W1 = np.load(os.path.join(folder_path, "W1.npy"))
        self.b1 = np.load(os.path.join(folder_path, "b1.npy"))
        self.W2 = np.load(os.path.join(folder_path, "W2.npy"))
        self.b2 = np.load(os.path.join(folder_path, "b2.npy"))
        print(f"Model loaded from {folder_path}")