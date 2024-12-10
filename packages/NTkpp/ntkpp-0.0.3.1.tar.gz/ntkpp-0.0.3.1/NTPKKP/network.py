import numpy as np


class NeuralNetwork:
    """
    Класс представляет собой нейронную сеть.

    Атрибуты:
    layers: list, список слоев нейронной сети.
    learning_rate: float, скорость обучения для обновления весов.
    """

    def __init__(self, learning_rate=0.01):
        """
        Инициализация класса NeuralNetwork.

        Параметры:
        learning_rate: float, скорость обучения, по умолчанию равна 0.01.
        """

        self.layers = []  # Инициируем пустой список для слоев сети
        self.learning_rate = learning_rate  # Устанавливаем скорость обучения

    def add_layer(self, layer):
        """
        Добавляет слой к нейронной сети.

        Параметры:
        layer: объект слоя, который будет добавлен в сеть.
        """

        self.layers.append(layer)  # Добавляем слой в список слоев

    def forward(self, X):
        """
        Прямое распространение входных данных через нейронную сеть.

        Параметры:
        X: ndarray, входные данные (размерность: [количество образцов, количество признаков]).

        Возвращает:
        output: ndarray, выходные данные сети после применения всех слоев.
        """

        output = X  # Начальное значение - входные данные
        for layer in self.layers:
            output = layer.forward(output)  # Применяем каждый слой
        return output  # Возвращаем выходные данные

    def backward(self, X, y, loss_func):
        """
        Обратное распространение потерь через нейронную сеть.

        Параметры:
        X: ndarray, входные данные (размерность: [количество образцов, количество признаков]).
        y: ndarray, целевые данные (размерность: [количество образцов, количество выходов]).
        loss_func: объект функции потерь, используемый для вычисления градиента.

        """

        output = self.forward(X)  # Получаем выходные данные для входных данных
        loss_gradient = loss_func.gradient(y, output)  # Вычисляем градиент потерь
        for layer in reversed(self.layers):
            loss_gradient = layer.backward(loss_gradient)  # Обратное распространение градиента

    def update_weights(self):
        """
        Обновляет веса всех слоев нейронной сети с учетом заданной скорости обучения.
        """

        for layer in self.layers:
            if hasattr(layer, 'update_weights'):
                layer.update_weights(self.learning_rate)  # Обновляем веса слоя
